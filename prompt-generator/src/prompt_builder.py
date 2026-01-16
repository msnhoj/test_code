"""Prompt builder that assembles prompts from user inputs and templates."""

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from config import TEMPLATES_DIR


@dataclass
class PromptContext:
    """Holds all context for building a prompt."""

    category: str = ""
    language: str = ""
    framework: str = ""
    code_snippet: str = ""
    answers: dict = field(default_factory=dict)


class PromptBuilder:
    """Builds coding prompts from templates and user input."""

    def __init__(self, templates_path: Optional[Path] = None):
        """Initialize the prompt builder.

        Args:
            templates_path: Path to templates directory.
        """
        self.templates_path = templates_path or TEMPLATES_DIR
        self.templates = self._load_templates()

    def _load_templates(self) -> dict:
        """Load templates from JSON file."""
        templates_file = self.templates_path / "coding_templates.json"

        if not templates_file.exists():
            raise FileNotFoundError(f"Templates file not found: {templates_file}")

        with open(templates_file, "r") as f:
            return json.load(f)

    def get_categories(self) -> list[dict]:
        """Get available prompt categories.

        Returns:
            List of category dictionaries with id, name, and description.
        """
        categories = []
        for cat_id, cat_data in self.templates["categories"].items():
            categories.append({
                "id": cat_id,
                "name": cat_data["name"],
                "description": cat_data["description"]
            })
        return categories

    def get_category_questions(self, category_id: str) -> list[dict]:
        """Get questions for a specific category.

        Args:
            category_id: The category identifier.

        Returns:
            List of question dictionaries.
        """
        if category_id not in self.templates["categories"]:
            raise ValueError(f"Unknown category: {category_id}")

        return self.templates["categories"][category_id]["questions"]

    def get_languages(self) -> list[str]:
        """Get available programming languages."""
        return self.templates["languages"]

    def get_frameworks(self, language: str) -> list[str]:
        """Get frameworks for a given language.

        Args:
            language: The programming language.

        Returns:
            List of available frameworks.
        """
        frameworks = self.templates.get("frameworks", {})
        return frameworks.get(language, frameworks.get("default", ["None/Vanilla"]))

    def build_prompt(self, context: PromptContext) -> str:
        """Build a complete prompt from context.

        Args:
            context: PromptContext with all gathered information.

        Returns:
            The formatted prompt string.
        """
        if context.category not in self.templates["categories"]:
            raise ValueError(f"Unknown category: {context.category}")

        template = self.templates["categories"][context.category]["template"]

        # Build substitution dictionary
        substitutions = {
            "language": context.language,
            "framework": context.framework,
            "code_snippet": context.code_snippet or "# No code provided",
            **context.answers
        }

        # Substitute all placeholders
        prompt = template
        for key, value in substitutions.items():
            placeholder = "{" + key + "}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value) if value else "N/A")

        return prompt

    def validate_context(self, context: PromptContext) -> list[str]:
        """Validate that context has required information.

        Args:
            context: The context to validate.

        Returns:
            List of missing required fields.
        """
        missing = []

        if not context.category:
            missing.append("category")
            return missing  # Can't check questions without category

        if not context.language:
            missing.append("language")

        # Check required questions
        questions = self.get_category_questions(context.category)
        for q in questions:
            if q.get("required", False) and q["id"] not in context.answers:
                missing.append(q["id"])

        return missing

    def get_prompt_suggestions(self, context: PromptContext) -> list[str]:
        """Get suggestions for improving the prompt.

        Args:
            context: Current prompt context.

        Returns:
            List of suggestions.
        """
        suggestions = []

        if not context.code_snippet:
            suggestions.append(
                "Consider adding a code snippet for more specific assistance."
            )

        if context.framework == "None/Vanilla":
            suggestions.append(
                "If you're using any libraries, mentioning them can help get more relevant solutions."
            )

        # Check for short answers
        for key, value in context.answers.items():
            if isinstance(value, str) and len(value) < 20:
                suggestions.append(
                    f"The '{key}' answer is brief. More detail could improve the response."
                )

        return suggestions

    def format_for_cli(self, prompt: str) -> str:
        """Format prompt for use with Claude CLI.

        Args:
            prompt: The built prompt.

        Returns:
            Formatted string for CLI usage.
        """
        # Escape special characters for shell
        escaped = prompt.replace("'", "'\\''")
        return f"claude '{escaped}'"

    def format_for_file(self, prompt: str, filename: str = "prompt.md") -> tuple[str, str]:
        """Format prompt for saving to file.

        Args:
            prompt: The built prompt.
            filename: Output filename.

        Returns:
            Tuple of (filename, formatted content).
        """
        header = """# Generated Coding Prompt

> Generated by Prompt Generator for VS Code + Claude
> Copy this prompt to Claude Chat or Claude CLI

---

"""
        return filename, header + prompt

    def export_prompt(self, prompt: str, format_type: str = "markdown") -> str:
        """Export prompt in various formats.

        Args:
            prompt: The built prompt.
            format_type: One of 'markdown', 'plain', 'json'.

        Returns:
            Formatted prompt string.
        """
        if format_type == "plain":
            return prompt

        if format_type == "json":
            return json.dumps({
                "prompt": prompt,
                "format": "coding_assistance",
                "generator": "prompt-generator-vscode"
            }, indent=2)

        # Default to markdown
        return f"""# Coding Prompt

{prompt}

---
*Generated with Prompt Generator for VS Code + Claude*
"""
