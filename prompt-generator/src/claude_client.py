"""Claude API client wrapper for the prompt generator."""

from typing import Optional, Generator
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS


class ClaudeClient:
    """Client for interacting with Claude API."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the Claude client.

        Args:
            api_key: Anthropic API key. Uses env var if not provided.
            model: Model to use. Defaults to configured model.
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.model = model or CLAUDE_MODEL

        if not self.api_key:
            raise ValueError(
                "API key is required. Set ANTHROPIC_API_KEY in .env or pass directly."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def send_message(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = MAX_TOKENS,
    ) -> str:
        """Send a message to Claude and get a response.

        Args:
            prompt: The user prompt to send.
            system_prompt: Optional system prompt for context.
            max_tokens: Maximum tokens in response.

        Returns:
            The response text from Claude.
        """
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def send_message_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = MAX_TOKENS,
    ) -> Generator[str, None, None]:
        """Send a message and stream the response.

        Args:
            prompt: The user prompt to send.
            system_prompt: Optional system prompt for context.
            max_tokens: Maximum tokens in response.

        Yields:
            Text chunks as they arrive.
        """
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text

    def refine_prompt(self, original_prompt: str, feedback: str) -> str:
        """Help refine a prompt based on user feedback.

        Args:
            original_prompt: The original prompt that needs refinement.
            feedback: User feedback on what to improve.

        Returns:
            Suggestions for improving the prompt.
        """
        system = """You are a prompt engineering expert. Your job is to help users
create more effective prompts for coding assistance. Analyze the given prompt and
feedback, then provide specific suggestions for improvement. Focus on:
1. Clarity and specificity
2. Missing context that would help
3. Better structure or organization
4. More actionable requests"""

        refinement_request = f"""Original prompt:
{original_prompt}

User feedback:
{feedback}

Please suggest how to improve this prompt to get better coding assistance."""

        return self.send_message(refinement_request, system_prompt=system)

    def analyze_prompt_quality(self, prompt: str) -> dict:
        """Analyze the quality of a prompt and provide scores.

        Args:
            prompt: The prompt to analyze.

        Returns:
            Dictionary with quality scores and suggestions.
        """
        system = """You are a prompt quality analyzer. Evaluate the given prompt
for coding assistance and provide a JSON response with:
- clarity_score (1-10)
- specificity_score (1-10)
- context_score (1-10)
- actionability_score (1-10)
- overall_score (1-10)
- missing_elements (list of strings)
- suggestions (list of strings)

Respond ONLY with valid JSON, no other text."""

        analysis_request = f"Analyze this coding prompt:\n\n{prompt}"

        response = self.send_message(analysis_request, system_prompt=system)

        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "error": "Could not parse analysis",
                "raw_response": response
            }
