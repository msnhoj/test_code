# Prompt Generator for VS Code + Claude

A standalone tool for creating effective, well-structured prompts for coding assistance with Claude CLI and Claude Chat. This tool helps you articulate specific coding needs, avoid vague requests, and iteratively refine your prompts for better results.

## Features

- **Guided Prompt Creation**: Step-by-step wizard for 8 different coding scenarios
- **Quick Prompt Mode**: Freeform prompt entry with quality analysis
- **Iterative Refinement**: Improve prompts based on structured feedback
- **Quality Analysis**: Score and analyze prompts before sending
- **Claude API Integration**: Send prompts directly to Claude and receive responses
- **Multiple Export Formats**: Markdown, plain text, JSON, or CLI-ready format

## Supported Coding Scenarios

1. **Debug & Fix Issues** - Identify and resolve bugs, errors, unexpected behavior
2. **Implement New Features** - Build new functionality with clear requirements
3. **Code Review** - Get feedback on quality, patterns, and best practices
4. **Refactor Code** - Improve structure, readability, or performance
5. **Explain Code/Concepts** - Understand code or learn programming concepts
6. **Write Tests** - Create unit, integration, or end-to-end tests
7. **Design APIs** - Design REST, GraphQL, or function interfaces
8. **Optimize Performance** - Improve speed, memory, or efficiency

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Clone or download this folder** to your local machine

2. **Navigate to the folder**:
   ```bash
   cd prompt-generator
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv

   # On macOS/Linux:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure your API key**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

   > Get your API key from: https://console.anthropic.com/

## Usage

### Running the Application

```bash
python run.py
```

### Main Menu Options

```
┌──────────────────────────────────────────────┐
│ 1 │ Create New Prompt (Guided)               │
│ 2 │ Quick Prompt (Freeform)                  │
│ 3 │ Refine Existing Prompt                   │
│ 4 │ Analyze Prompt Quality                   │
│ 5 │ Send to Claude (requires API key)        │
│ 6 │ Export Last Prompt                       │
│ 7 │ View Templates                           │
│ q │ Quit                                     │
└──────────────────────────────────────────────┘
```

### Guided Prompt Creation

The guided mode walks you through:

1. **Category Selection** - Choose your task type (debugging, feature, review, etc.)
2. **Language Selection** - Pick from 18 programming languages
3. **Framework Selection** - Choose relevant frameworks for your language
4. **Contextual Questions** - Answer category-specific questions
5. **Code Snippet** - Optionally include relevant code

### Quick Prompt Mode

For when you know what you want to ask:

1. Enter your prompt directly (multi-line supported)
2. Press Enter twice to finish
3. Optionally analyze the prompt quality
4. Refine if needed

### Prompt Refinement

Improve existing prompts by adding:

- **Context** - Background information
- **Code** - Relevant code snippets
- **Clarification** - Additional details
- **Constraints** - Technical requirements
- **Error details** - Error messages and stack traces

### Quality Analysis

The analyzer scores your prompt on:

- **Specificity** (0-25) - How specific and detailed
- **Context** (0-25) - Background information provided
- **Actionability** (0-25) - Clear request for action
- **Structure** (0-25) - Organization and formatting

Scores of 80+ indicate excellent prompts.

## Example Workflow

### Debugging Example

1. Select "Create New Prompt (Guided)"
2. Choose "Debug & Fix Issues"
3. Select "Python" and "Django"
4. Answer questions:
   - Error type: Runtime error
   - Error message: "TypeError: 'NoneType' object is not subscriptable"
   - Expected: User data returned from API
   - Actual: Crashes when user not found
5. Add your code snippet
6. Review generated prompt
7. Send to Claude or export

### Generated Prompt Example

```markdown
I need help debugging a Runtime error in my code.

**Error Message:**
TypeError: 'NoneType' object is not subscriptable

**Expected Behavior:**
User data returned from API

**Actual Behavior:**
Crashes when user not found

**Steps to Reproduce:**
1. Call /api/users/999 with non-existent ID

**What I've Tried:**
Added null check but still failing

**Relevant Code:**
```python
def get_user(user_id):
    user = User.objects.filter(id=user_id).first()
    return user['name']  # Crashes here
```

Please help me identify the root cause and provide a fix.
```

## Using with Claude CLI

Export your prompt in CLI format:

```bash
claude 'Your generated prompt here...'
```

Or pipe from a file:

```bash
claude < output/prompt_20240115_143022.md
```

## Using with Claude Chat

1. Export to Markdown format
2. Copy the content from `output/prompt_*.md`
3. Paste into Claude Chat at https://claude.ai

## Configuration Options

Edit `.env` to customize:

```bash
# Required: Your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Default model (default: claude-sonnet-4-20250514)
CLAUDE_MODEL=claude-sonnet-4-20250514

# Optional: Max response tokens (default: 4096)
MAX_TOKENS=4096
```

### Available Models

- `claude-sonnet-4-20250514` - Fast, intelligent (recommended)
- `claude-opus-4-20250514` - Most capable
- `claude-3-5-sonnet-20241022` - Previous generation
- `claude-3-5-haiku-20241022` - Fastest, most economical

## Project Structure

```
prompt-generator/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration management
├── src/
│   ├── __init__.py
│   ├── claude_client.py     # Claude API wrapper
│   ├── main.py              # Interactive CLI application
│   ├── prompt_builder.py    # Prompt construction logic
│   └── refinement_engine.py # Iterative refinement system
├── templates/
│   └── coding_templates.json # Prompt templates and questions
├── output/                   # Generated prompts (auto-created)
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt
├── run.py                   # Entry point
└── README.md
```

## Extending Templates

Add custom templates by editing `templates/coding_templates.json`:

```json
{
  "categories": {
    "my_custom_task": {
      "name": "My Custom Task",
      "description": "Description of what this helps with",
      "questions": [
        {
          "id": "question_id",
          "question": "What is your question?",
          "type": "text",
          "required": true
        }
      ],
      "template": "Template with {question_id} placeholders..."
    }
  }
}
```

## Tips for Effective Prompts

1. **Be Specific** - Replace "it doesn't work" with exact error messages
2. **Provide Context** - Include language versions, frameworks, dependencies
3. **Show Your Code** - Include relevant code snippets with proper formatting
4. **State Your Goal** - Explain what you're trying to achieve
5. **Mention Constraints** - Note any requirements or limitations
6. **Share What You Tried** - List solutions you've already attempted

## Troubleshooting

### "API key not configured"

Ensure you've:
1. Copied `.env.example` to `.env`
2. Added your actual API key to `.env`
3. The key starts with `sk-ant-`

### "Module not found" errors

Ensure you've:
1. Activated your virtual environment
2. Installed dependencies with `pip install -r requirements.txt`

### Rich/prompt_toolkit display issues

On Windows, ensure you're using Windows Terminal or a terminal that supports ANSI colors.

## License

MIT License - Feel free to modify and use as needed.

## Contributing

Contributions welcome! Areas for improvement:

- Additional prompt templates
- VS Code extension integration
- Web interface
- Prompt history and favorites
- Team sharing features
