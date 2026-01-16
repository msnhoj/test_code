"""Configuration settings for the prompt generator."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

# Application Settings
APP_NAME = "Prompt Generator for VS Code + Claude"
APP_VERSION = "1.0.0"

# Available models
AVAILABLE_MODELS = [
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
]

def validate_config():
    """Validate that required configuration is present."""
    errors = []

    if not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is not set. Please add it to your .env file.")

    if CLAUDE_MODEL not in AVAILABLE_MODELS:
        errors.append(f"Invalid model: {CLAUDE_MODEL}. Available: {', '.join(AVAILABLE_MODELS)}")

    return errors
