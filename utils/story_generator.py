from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Import the template
from utils.templates.story_template import STORY_TEMPLATE

# Load environment variables from .env file
load_dotenv()

class ChatApplication:
    def __init__(self, template=None):
        # Get API key from environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        # Initialize OpenAI API key
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Initialize the language model (GPT-4)
        self.llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.7
        )
        
        # Set template
        self.template = template or STORY_TEMPLATE
            
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_template(self.template)
        
        # Create the chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=True
        )
        
        # Initialize story context
        self.story_context = []
    
    def generate_story(self, story_data, feedback="", previous_chapter=""):
        """
        Generate a story based on the provided data and feedback
        """
        # Format main characters for better readability
        characters_text = "\n".join(
            f"- {char['name']}: {char['description']}" for char in story_data["main_characters"]
        )
        
        # Prepare the input data
        input_data = {
            "title": story_data["title"],
            "genre": story_data["genre"],
            "main_characters": characters_text,
            "facts": story_data["introduction"]["facts"],
            "outcome": story_data["introduction"]["outcome"],
            "story_beginning": story_data["story_beginning"],
            "feedback": feedback,
            "previous_chapter": previous_chapter
        }
        
        # Generate the story
        response = self.chain.run(input_data)
        return response