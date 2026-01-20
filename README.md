# Essentials - AI Post Generator

A Python application that uses Google's Gemini API to generate social media posts.

## Prerequisites

- Python 3.12 or higher
- Google Gemini API key

## Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd essentials
   ```

2. **Install dependencies**

   ```bash
   pip install -e .
   ```

   Or with uv:

   ```bash
   uv sync
   ```

3. **Configure environment variables**

   Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Google Gemini API key:

   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

   **Get your API key:** Visit [Google AI Studio](https://aistudio.google.com/app/apikey)

## Usage

Run the application:

```bash
python main.py
```

The application will prompt you for a topic and generate a social media post using Gemini AI.

## Security Notes

⚠️ **NEVER commit your `.env` file to git!**

The `.env` file contains sensitive API keys and is already listed in `.gitignore`. Always use `.env.example` as a template for required environment variables.

## Project Structure

- `main.py` - Main application entry point
- `.env.example` - Template for environment variables
- `pyproject.toml` - Project dependencies and metadata
