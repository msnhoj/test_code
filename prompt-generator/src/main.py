"""Main interactive application for the prompt generator."""

import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from prompt_toolkit import prompt as pt_prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from config import APP_NAME, APP_VERSION, OUTPUT_DIR, validate_config, ANTHROPIC_API_KEY
from .prompt_builder import PromptBuilder, PromptContext
from .refinement_engine import RefinementEngine


console = Console()


class PromptGeneratorApp:
    """Interactive prompt generator application."""

    def __init__(self):
        """Initialize the application."""
        self.builder = PromptBuilder()
        self.engine = RefinementEngine(self.builder)
        self.context = PromptContext()
        self.current_prompt: Optional[str] = None
        self.claude_client = None

        # Setup history for multiline input
        history_file = OUTPUT_DIR / ".prompt_history"
        self.history = FileHistory(str(history_file))

    def display_header(self):
        """Display the application header."""
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]{APP_NAME}[/bold cyan]\n"
            f"[dim]Version {APP_VERSION}[/dim]",
            border_style="cyan"
        ))
        console.print()

    def display_menu(self) -> str:
        """Display main menu and get choice.

        Returns:
            User's menu choice.
        """
        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        table.add_column("Option", style="bold yellow")
        table.add_column("Description")

        table.add_row("1", "Create New Prompt (Guided)")
        table.add_row("2", "Quick Prompt (Freeform)")
        table.add_row("3", "Refine Existing Prompt")
        table.add_row("4", "Analyze Prompt Quality")
        table.add_row("5", "Send to Claude (requires API key)")
        table.add_row("6", "Export Last Prompt")
        table.add_row("7", "View Templates")
        table.add_row("q", "Quit")

        console.print(table)
        console.print()

        return Prompt.ask(
            "[bold cyan]Select option[/bold cyan]",
            choices=["1", "2", "3", "4", "5", "6", "7", "q"],
            default="1"
        )

    def select_category(self) -> str:
        """Display category selection and get choice.

        Returns:
            Selected category ID.
        """
        categories = self.builder.get_categories()

        console.print("\n[bold]Select a task category:[/bold]\n")

        table = Table(show_header=True, box=box.ROUNDED)
        table.add_column("#", style="bold yellow", width=3)
        table.add_column("Category", style="cyan")
        table.add_column("Description")

        for i, cat in enumerate(categories, 1):
            table.add_row(str(i), cat["name"], cat["description"])

        console.print(table)
        console.print()

        choice = Prompt.ask(
            "[bold]Enter number[/bold]",
            choices=[str(i) for i in range(1, len(categories) + 1)]
        )

        return categories[int(choice) - 1]["id"]

    def select_language(self) -> str:
        """Display language selection.

        Returns:
            Selected programming language.
        """
        languages = self.builder.get_languages()

        console.print("\n[bold]Select programming language:[/bold]\n")

        # Display in columns
        cols = 3
        rows = []
        for i in range(0, len(languages), cols):
            row = languages[i:i+cols]
            rows.append(row)

        table = Table(show_header=False, box=None)
        for _ in range(cols):
            table.add_column(width=20)

        for row in rows:
            formatted = [f"[yellow]{i+1}.[/yellow] {lang}"
                        for i, lang in enumerate(row, start=rows.index(row)*cols)]
            # Pad row if needed
            while len(formatted) < cols:
                formatted.append("")
            table.add_row(*formatted)

        console.print(table)
        console.print()

        choice = Prompt.ask(
            "[bold]Enter number[/bold]",
            choices=[str(i) for i in range(1, len(languages) + 1)]
        )

        return languages[int(choice) - 1]

    def select_framework(self, language: str) -> str:
        """Display framework selection for a language.

        Args:
            language: The selected programming language.

        Returns:
            Selected framework.
        """
        frameworks = self.builder.get_frameworks(language)

        console.print(f"\n[bold]Select framework for {language}:[/bold]\n")

        for i, fw in enumerate(frameworks, 1):
            console.print(f"  [yellow]{i}.[/yellow] {fw}")

        console.print()

        choice = Prompt.ask(
            "[bold]Enter number[/bold]",
            choices=[str(i) for i in range(1, len(frameworks) + 1)]
        )

        return frameworks[int(choice) - 1]

    def ask_questions(self, category: str) -> dict:
        """Ask category-specific questions.

        Args:
            category: The selected category.

        Returns:
            Dictionary of answers.
        """
        questions = self.builder.get_category_questions(category)
        answers = {}

        console.print("\n[bold]Please answer the following questions:[/bold]\n")

        for q in questions:
            required = q.get("required", False)
            req_marker = "[red]*[/red]" if required else ""

            console.print(f"\n{req_marker} [cyan]{q['question']}[/cyan]")

            if "options" in q:
                # Multiple choice
                for i, opt in enumerate(q["options"], 1):
                    console.print(f"  [yellow]{i}.[/yellow] {opt}")

                valid_choices = [str(i) for i in range(1, len(q["options"]) + 1)]
                if not required:
                    valid_choices.append("")

                choice = Prompt.ask(
                    "Enter number",
                    choices=valid_choices,
                    default="" if not required else None
                )

                if choice:
                    answers[q["id"]] = q["options"][int(choice) - 1]
            else:
                # Free text
                if required:
                    while True:
                        answer = pt_prompt(
                            "> ",
                            history=self.history,
                            auto_suggest=AutoSuggestFromHistory(),
                            multiline=False
                        )
                        if answer.strip():
                            answers[q["id"]] = answer.strip()
                            break
                        console.print("[red]This field is required.[/red]")
                else:
                    answer = pt_prompt(
                        "> (press Enter to skip) ",
                        history=self.history,
                        auto_suggest=AutoSuggestFromHistory(),
                        multiline=False
                    )
                    if answer.strip():
                        answers[q["id"]] = answer.strip()

        return answers

    def get_code_snippet(self) -> str:
        """Get code snippet from user.

        Returns:
            The code snippet.
        """
        console.print("\n[bold cyan]Enter your code snippet:[/bold cyan]")
        console.print("[dim](Enter your code, then press Enter twice to finish)[/dim]\n")

        lines = []
        empty_count = 0

        while True:
            try:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                    lines.append(line)
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break

        return "\n".join(lines).strip()

    def create_guided_prompt(self):
        """Create a prompt using the guided wizard."""
        console.print("\n[bold green]Starting Guided Prompt Creation[/bold green]\n")

        # Select category
        self.context.category = self.select_category()

        # Select language
        self.context.language = self.select_language()

        # Select framework
        self.context.framework = self.select_framework(self.context.language)

        # Ask category questions
        self.context.answers = self.ask_questions(self.context.category)

        # Get code snippet
        if Confirm.ask("\n[cyan]Would you like to include a code snippet?[/cyan]"):
            self.context.code_snippet = self.get_code_snippet()

        # Build the prompt
        self.current_prompt = self.builder.build_prompt(self.context)

        # Show suggestions
        suggestions = self.builder.get_prompt_suggestions(self.context)
        if suggestions:
            console.print("\n[yellow]Suggestions for improvement:[/yellow]")
            for s in suggestions:
                console.print(f"  - {s}")

        # Display the prompt
        self.display_prompt()

    def create_quick_prompt(self):
        """Create a quick freeform prompt."""
        console.print("\n[bold green]Quick Prompt Mode[/bold green]")
        console.print("[dim]Enter your prompt directly. Press Enter twice to finish.[/dim]\n")

        lines = []
        empty_count = 0

        while True:
            try:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                    lines.append(line)
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break

        self.current_prompt = "\n".join(lines).strip()

        if self.current_prompt:
            self.display_prompt()

            # Offer analysis
            if Confirm.ask("\n[cyan]Would you like to analyze this prompt?[/cyan]"):
                self.analyze_prompt()

    def refine_prompt(self):
        """Refine an existing prompt."""
        if not self.current_prompt:
            console.print("[yellow]No current prompt. Create one first.[/yellow]")
            return

        console.print("\n[bold green]Prompt Refinement[/bold green]\n")

        # Start refinement session
        self.engine.start_refinement(self.current_prompt)

        # Get refinement suggestions
        if self.context.category:
            suggestions = self.engine.suggest_refinements(self.context)

            if suggestions:
                console.print("[bold]Suggested refinements:[/bold]\n")

                table = Table(box=box.ROUNDED)
                table.add_column("#", style="yellow", width=3)
                table.add_column("Type", style="cyan")
                table.add_column("Suggestion")

                for i, s in enumerate(suggestions, 1):
                    table.add_row(str(i), s["type"], s["title"])

                console.print(table)

        # Ask for refinement type
        console.print("\n[bold]Refinement options:[/bold]")
        console.print("  [yellow]1.[/yellow] Add context")
        console.print("  [yellow]2.[/yellow] Add code")
        console.print("  [yellow]3.[/yellow] Add clarification")
        console.print("  [yellow]4.[/yellow] Add constraint")
        console.print("  [yellow]5.[/yellow] Add error details")
        console.print("  [yellow]6.[/yellow] Custom addition")

        choice = Prompt.ask(
            "\n[bold]Select refinement type[/bold]",
            choices=["1", "2", "3", "4", "5", "6"]
        )

        type_map = {
            "1": "context",
            "2": "code",
            "3": "clarify",
            "4": "constraint",
            "5": "error",
            "6": "custom"
        }

        ref_type = type_map[choice]

        console.print(f"\n[cyan]Enter your {ref_type}:[/cyan]")
        console.print("[dim](Press Enter twice to finish)[/dim]\n")

        lines = []
        empty_count = 0

        while True:
            try:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                    lines.append(line)
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break

        refinement_value = "\n".join(lines).strip()

        if refinement_value:
            self.current_prompt = self.engine.apply_refinement(
                self.current_prompt,
                ref_type,
                refinement_value
            )
            console.print("\n[green]Prompt refined successfully![/green]")
            self.display_prompt()

    def analyze_prompt(self):
        """Analyze the current prompt quality."""
        if not self.current_prompt:
            console.print("[yellow]No current prompt. Create one first.[/yellow]")
            return

        console.print("\n[bold green]Prompt Analysis[/bold green]\n")

        # Get analysis
        analysis = self.engine.analyze_prompt(self.current_prompt)
        scores = self.engine.score_prompt(self.current_prompt)

        # Display scores
        table = Table(title="Quality Scores", box=box.ROUNDED)
        table.add_column("Dimension", style="cyan")
        table.add_column("Score", justify="right")
        table.add_column("Bar", width=20)

        for dim, score in scores.items():
            if dim != "overall":
                bar = "█" * (score) + "░" * (25 - score)
                table.add_row(dim.title(), f"{score}/25", bar)

        console.print(table)

        console.print(f"\n[bold]Overall Score: {scores['overall']}/100[/bold]")

        # Quality indicator
        if scores["overall"] >= 80:
            console.print("[green]Excellent prompt quality![/green]")
        elif scores["overall"] >= 60:
            console.print("[yellow]Good prompt, could be improved.[/yellow]")
        else:
            console.print("[red]Prompt needs more detail.[/red]")

        # Show issues and suggestions
        if analysis["issues"]:
            console.print("\n[bold red]Issues Found:[/bold red]")
            for issue in analysis["issues"]:
                console.print(f"  - {issue}")

        if analysis["suggestions"]:
            console.print("\n[bold yellow]Suggestions:[/bold yellow]")
            for suggestion in analysis["suggestions"]:
                console.print(f"  - {suggestion}")

        # Offer refinement
        if scores["overall"] < 80:
            if Confirm.ask("\n[cyan]Would you like to refine this prompt?[/cyan]"):
                self.refine_prompt()

    def send_to_claude(self):
        """Send the current prompt to Claude API."""
        if not self.current_prompt:
            console.print("[yellow]No current prompt. Create one first.[/yellow]")
            return

        if not ANTHROPIC_API_KEY:
            console.print("[red]API key not configured. Add ANTHROPIC_API_KEY to .env file.[/red]")
            return

        # Initialize client if needed
        if not self.claude_client:
            try:
                from .claude_client import ClaudeClient
                self.claude_client = ClaudeClient()
            except Exception as e:
                console.print(f"[red]Failed to initialize Claude client: {e}[/red]")
                return

        console.print("\n[bold green]Sending to Claude...[/bold green]\n")

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Waiting for response...", total=None)

                response = self.claude_client.send_message(
                    self.current_prompt,
                    system_prompt="You are an expert coding assistant. Provide clear, well-structured responses with code examples when appropriate."
                )

                progress.remove_task(task)

            console.print(Panel(
                Markdown(response),
                title="[bold cyan]Claude's Response[/bold cyan]",
                border_style="green"
            ))

            # Offer to save
            if Confirm.ask("\n[cyan]Save response to file?[/cyan]"):
                filename = OUTPUT_DIR / f"response_{self._timestamp()}.md"
                with open(filename, "w") as f:
                    f.write(f"# Prompt\n\n{self.current_prompt}\n\n---\n\n# Response\n\n{response}")
                console.print(f"[green]Saved to {filename}[/green]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def export_prompt(self):
        """Export the current prompt to file."""
        if not self.current_prompt:
            console.print("[yellow]No current prompt. Create one first.[/yellow]")
            return

        console.print("\n[bold]Export format:[/bold]")
        console.print("  [yellow]1.[/yellow] Markdown")
        console.print("  [yellow]2.[/yellow] Plain text")
        console.print("  [yellow]3.[/yellow] JSON")
        console.print("  [yellow]4.[/yellow] Copy-ready for CLI")

        choice = Prompt.ask(
            "\n[bold]Select format[/bold]",
            choices=["1", "2", "3", "4"],
            default="1"
        )

        format_map = {"1": "markdown", "2": "plain", "3": "json", "4": "cli"}
        format_type = format_map[choice]

        if format_type == "cli":
            cli_command = self.builder.format_for_cli(self.current_prompt)
            console.print("\n[bold]CLI Command:[/bold]")
            console.print(Panel(cli_command, border_style="cyan"))
        else:
            content = self.builder.export_prompt(self.current_prompt, format_type)

            ext_map = {"markdown": "md", "plain": "txt", "json": "json"}
            filename = OUTPUT_DIR / f"prompt_{self._timestamp()}.{ext_map[format_type]}"

            with open(filename, "w") as f:
                f.write(content)

            console.print(f"\n[green]Exported to {filename}[/green]")

    def view_templates(self):
        """View available templates."""
        categories = self.builder.get_categories()

        console.print("\n[bold]Available Templates:[/bold]\n")

        for cat in categories:
            console.print(Panel(
                f"[bold]{cat['name']}[/bold]\n\n{cat['description']}\n\n"
                f"[dim]Questions: {len(self.builder.get_category_questions(cat['id']))}[/dim]",
                border_style="cyan"
            ))

    def display_prompt(self):
        """Display the current prompt."""
        if not self.current_prompt:
            console.print("[yellow]No prompt generated yet.[/yellow]")
            return

        console.print("\n" + "="*60)
        console.print(Panel(
            Markdown(self.current_prompt),
            title="[bold cyan]Generated Prompt[/bold cyan]",
            border_style="green"
        ))
        console.print("="*60 + "\n")

    def _timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def run(self):
        """Run the main application loop."""
        self.display_header()

        # Validate configuration
        errors = validate_config()
        if errors:
            console.print("[yellow]Configuration warnings:[/yellow]")
            for error in errors:
                console.print(f"  - {error}")
            console.print()

        while True:
            try:
                choice = self.display_menu()

                if choice == "q":
                    console.print("\n[cyan]Goodbye![/cyan]\n")
                    break
                elif choice == "1":
                    self.create_guided_prompt()
                elif choice == "2":
                    self.create_quick_prompt()
                elif choice == "3":
                    self.refine_prompt()
                elif choice == "4":
                    self.analyze_prompt()
                elif choice == "5":
                    self.send_to_claude()
                elif choice == "6":
                    self.export_prompt()
                elif choice == "7":
                    self.view_templates()

            except KeyboardInterrupt:
                console.print("\n[yellow]Operation cancelled.[/yellow]")
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")


def main():
    """Entry point for the application."""
    app = PromptGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()
