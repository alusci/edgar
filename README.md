# Edgar: Story Generator

A Python application that generates story scenes using OpenAI's GPT-4 model and LangChain. The application takes story elements (characters, background, etc.) as input and generates the next scene while maintaining consistency with the established narrative.

## Prerequisites

- Python 3.11 or higher
- Conda package manager
- OpenAI API key

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a conda environment:
```bash
conda create -n story-gen python=3.11
conda activate story-gen
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

```

## Usage

1. Make sure your conda environment is activated:
```bash
conda activate story-gen
```

2. Prepare your story data:
   - Use the provided example in `data/inputs/stone_giant_heroons.json` as a template
   - Create your own JSON file following the same structure
   - Required fields: title, genre, main_characters, introduction (facts, outcome), story_beginning

3. Run the application:
```bash
python main.py
```

## Input Data Structure

The input JSON should follow this structure:
```json
{
    "title": "Your Story Title",
    "genre": "Genre / Sub-genre",
    "main_characters": [
        {
            "name": "Character Name",
            "description": "Character description"
        }
    ],
    "introduction": {
        "facts": "Background information",
        "outcome": "Known outcome or future events"
    },
    "story_beginning": "The current scene or starting point"
}
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Note

Make sure to keep your `.env` file secure and never commit it to version control. The `.gitignore` file is configured to exclude it automatically.
