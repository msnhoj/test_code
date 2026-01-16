"""Iterative refinement engine for improving prompts."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .prompt_builder import PromptBuilder, PromptContext


@dataclass
class RefinementHistory:
    """Tracks the history of prompt refinements."""

    original_prompt: str
    iterations: list = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def add_iteration(self, prompt: str, feedback: str, suggestions: list[str]):
        """Add a refinement iteration.

        Args:
            prompt: The refined prompt.
            feedback: User feedback that led to refinement.
            suggestions: Suggestions applied.
        """
        self.iterations.append({
            "prompt": prompt,
            "feedback": feedback,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        })

    def get_latest_prompt(self) -> str:
        """Get the most recent version of the prompt."""
        if self.iterations:
            return self.iterations[-1]["prompt"]
        return self.original_prompt

    def get_iteration_count(self) -> int:
        """Get the number of refinement iterations."""
        return len(self.iterations)


class RefinementEngine:
    """Engine for iteratively refining prompts based on feedback."""

    def __init__(self, prompt_builder: PromptBuilder):
        """Initialize the refinement engine.

        Args:
            prompt_builder: PromptBuilder instance to use.
        """
        self.builder = prompt_builder
        self.current_history: Optional[RefinementHistory] = None

    def start_refinement(self, initial_prompt: str) -> RefinementHistory:
        """Start a new refinement session.

        Args:
            initial_prompt: The initial prompt to refine.

        Returns:
            New RefinementHistory instance.
        """
        self.current_history = RefinementHistory(original_prompt=initial_prompt)
        return self.current_history

    def analyze_prompt(self, prompt: str) -> dict:
        """Analyze a prompt for potential improvements.

        Args:
            prompt: The prompt to analyze.

        Returns:
            Analysis results with suggestions.
        """
        analysis = {
            "issues": [],
            "suggestions": [],
            "score": 100
        }

        # Check for vague language
        vague_terms = ["help", "fix", "issue", "problem", "something", "thing"]
        prompt_lower = prompt.lower()
        for term in vague_terms:
            if f" {term} " in f" {prompt_lower} ":
                analysis["issues"].append(f"Vague term detected: '{term}'")
                analysis["suggestions"].append(f"Replace '{term}' with specific details")
                analysis["score"] -= 5

        # Check for missing context indicators
        context_indicators = {
            "error": "Include the exact error message",
            "code": "Include relevant code snippets",
            "expected": "Describe what you expected to happen",
            "tried": "Mention what you've already tried"
        }

        for indicator, suggestion in context_indicators.items():
            if indicator not in prompt_lower:
                analysis["suggestions"].append(suggestion)
                analysis["score"] -= 3

        # Check prompt length
        word_count = len(prompt.split())
        if word_count < 20:
            analysis["issues"].append("Prompt may be too brief")
            analysis["suggestions"].append("Add more context and details")
            analysis["score"] -= 10
        elif word_count > 500:
            analysis["issues"].append("Prompt may be too long")
            analysis["suggestions"].append("Consider breaking into smaller, focused requests")
            analysis["score"] -= 5

        # Check for code blocks
        if "```" not in prompt and any(kw in prompt_lower for kw in ["code", "function", "class", "error"]):
            analysis["suggestions"].append("Consider adding code blocks with triple backticks")
            analysis["score"] -= 5

        # Ensure score doesn't go below 0
        analysis["score"] = max(0, analysis["score"])

        return analysis

    def suggest_refinements(self, context: PromptContext) -> list[dict]:
        """Generate specific refinement suggestions based on context.

        Args:
            context: Current prompt context.

        Returns:
            List of refinement suggestions with details.
        """
        suggestions = []

        # Category-specific suggestions
        category_tips = {
            "debugging": [
                {
                    "type": "context",
                    "title": "Add Environment Info",
                    "description": "Include your OS, language version, and relevant dependency versions",
                    "example": "Python 3.11, Django 4.2, PostgreSQL 15"
                },
                {
                    "type": "context",
                    "title": "Include Stack Trace",
                    "description": "If there's an error, include the full stack trace",
                    "example": "```\nTraceback (most recent call last):\n  File...\n```"
                }
            ],
            "feature_implementation": [
                {
                    "type": "clarity",
                    "title": "Define Edge Cases",
                    "description": "Specify how the feature should handle unusual inputs",
                    "example": "If user enters negative number, show validation error"
                },
                {
                    "type": "structure",
                    "title": "Break Into Steps",
                    "description": "For complex features, list the implementation steps",
                    "example": "1. Create model, 2. Add API endpoint, 3. Build UI"
                }
            ],
            "code_review": [
                {
                    "type": "focus",
                    "title": "Specify Review Criteria",
                    "description": "Tell the reviewer what aspects matter most",
                    "example": "Focus on thread safety and memory management"
                }
            ],
            "refactoring": [
                {
                    "type": "context",
                    "title": "Explain Current Pain Points",
                    "description": "Describe specific issues with the current code",
                    "example": "This function is 200 lines and hard to test"
                }
            ],
            "explanation": [
                {
                    "type": "context",
                    "title": "Share Your Current Understanding",
                    "description": "Explain what you already know to get more targeted help",
                    "example": "I understand X does Y, but I'm confused about Z"
                }
            ],
            "testing": [
                {
                    "type": "requirements",
                    "title": "List Critical Scenarios",
                    "description": "Identify the most important test cases",
                    "example": "Must test: empty input, max length, special characters"
                }
            ],
            "api_design": [
                {
                    "type": "requirements",
                    "title": "Define Success Criteria",
                    "description": "Specify performance and reliability requirements",
                    "example": "Must handle 1000 req/s with <100ms latency"
                }
            ],
            "optimization": [
                {
                    "type": "metrics",
                    "title": "Include Benchmarks",
                    "description": "Share current performance measurements",
                    "example": "Currently takes 5s for 10k records, need <1s"
                }
            ]
        }

        if context.category in category_tips:
            suggestions.extend(category_tips[context.category])

        # Generic suggestions
        if not context.code_snippet:
            suggestions.append({
                "type": "required",
                "title": "Add Code Snippet",
                "description": "Include the relevant code for better assistance",
                "example": "```python\ndef your_function():\n    pass\n```"
            })

        return suggestions

    def apply_refinement(
        self,
        current_prompt: str,
        refinement_type: str,
        refinement_value: str
    ) -> str:
        """Apply a specific refinement to a prompt.

        Args:
            current_prompt: The current prompt text.
            refinement_type: Type of refinement (context, clarify, etc.).
            refinement_value: The refinement content to add.

        Returns:
            The refined prompt.
        """
        refinement_templates = {
            "context": "\n\n**Additional Context:**\n{value}",
            "code": "\n\n**Relevant Code:**\n```\n{value}\n```",
            "clarify": "\n\n**Clarification:**\n{value}",
            "constraint": "\n\n**Constraints:**\n{value}",
            "example": "\n\n**Example of Desired Output:**\n{value}",
            "error": "\n\n**Error Details:**\n```\n{value}\n```"
        }

        template = refinement_templates.get(
            refinement_type,
            "\n\n**{type}:**\n{value}"
        )

        addition = template.format(type=refinement_type.title(), value=refinement_value)
        refined_prompt = current_prompt + addition

        # Record in history if active
        if self.current_history:
            self.current_history.add_iteration(
                prompt=refined_prompt,
                feedback=f"Added {refinement_type}",
                suggestions=[f"Applied {refinement_type} refinement"]
            )

        return refined_prompt

    def get_refinement_questions(self, prompt: str) -> list[dict]:
        """Generate clarifying questions based on prompt analysis.

        Args:
            prompt: The prompt to analyze.

        Returns:
            List of clarifying questions.
        """
        questions = []
        prompt_lower = prompt.lower()

        # Check for missing common elements
        if "version" not in prompt_lower:
            questions.append({
                "id": "version",
                "question": "What version of the language/framework are you using?",
                "why": "Version-specific solutions are often more accurate"
            })

        if "tried" not in prompt_lower and "attempt" not in prompt_lower:
            questions.append({
                "id": "attempts",
                "question": "What approaches have you already tried?",
                "why": "Helps avoid suggesting things you've already ruled out"
            })

        if "error" in prompt_lower and "message" not in prompt_lower:
            questions.append({
                "id": "error_message",
                "question": "Can you share the exact error message?",
                "why": "Exact error messages help pinpoint the issue"
            })

        if "file" in prompt_lower or "import" in prompt_lower:
            questions.append({
                "id": "structure",
                "question": "Can you describe your project structure?",
                "why": "File organization affects import paths and solutions"
            })

        return questions

    def score_prompt(self, prompt: str) -> dict:
        """Score a prompt on various quality dimensions.

        Args:
            prompt: The prompt to score.

        Returns:
            Dictionary with dimension scores and overall score.
        """
        scores = {
            "specificity": 0,
            "context": 0,
            "actionability": 0,
            "structure": 0,
            "overall": 0
        }

        prompt_lower = prompt.lower()
        word_count = len(prompt.split())

        # Specificity (0-25)
        specificity = 15
        if any(x in prompt_lower for x in ["exact", "specific", "particular"]):
            specificity += 5
        if "```" in prompt:  # Has code blocks
            specificity += 5
        scores["specificity"] = min(25, specificity)

        # Context (0-25)
        context_score = 10
        context_keywords = ["using", "version", "environment", "framework", "library"]
        for kw in context_keywords:
            if kw in prompt_lower:
                context_score += 3
        scores["context"] = min(25, context_score)

        # Actionability (0-25)
        action_score = 10
        action_phrases = ["please", "help me", "how to", "i need", "create", "fix", "implement"]
        for phrase in action_phrases:
            if phrase in prompt_lower:
                action_score += 3
        scores["actionability"] = min(25, action_score)

        # Structure (0-25)
        structure_score = 10
        if "**" in prompt or "##" in prompt:  # Has formatting
            structure_score += 5
        if "\n\n" in prompt:  # Has paragraphs
            structure_score += 5
        if word_count > 30:  # Reasonable length
            structure_score += 5
        scores["structure"] = min(25, structure_score)

        # Overall
        scores["overall"] = sum([
            scores["specificity"],
            scores["context"],
            scores["actionability"],
            scores["structure"]
        ])

        return scores
