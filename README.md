# Newsletter Generator

An AI-powered newsletter generation system that automatically creates engaging newsletters using various data sources and AI capabilities.

## Features

- Automated content generation using AI
- Image generation for newsletter content
- Link fetching and content aggregation
- Customizable newsletter templates
- Docker support for easy deployment

## Project Structure

```
newsletter/
├── src/
│   └── newsletter/
│       ├── core/           # Core functionality
│       ├── templates/      # Newsletter templates
│       ├── utils/          # Utility functions
│       ├── config/        # Configuration files
│       └── main.py        # Application entry point
├── Dockerfile             # Docker configuration
├── compose.yaml          # Docker Compose configuration
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project metadata
└── .env                 # Environment variables (git-ignored)
```

## Prerequisites

- Python 3.10 or higher
- Docker (optional)
- OpenAI API key
- Other required API keys (as specified in .env)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd newsletter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

## Usage

### Running Locally

```bash
python src/newsletter/main.py
```

### Running with Docker

```bash
docker-compose up --build
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY=your_api_key_here
# Add other required API keys
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

[Add your license here]

## Authors

[Add authors here]
