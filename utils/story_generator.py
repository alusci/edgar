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
    def __init__(self, template=None, history_limit=10000):
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
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Maximum history length in characters
        self.history_limit = history_limit
    
    def _trim_history(self):
        """Trim history to keep it under the character limit"""
        current_length = sum(len(entry) for entry in self.conversation_history)
        
        while current_length > self.history_limit and len(self.conversation_history) > 2:
            # Remove the oldest entry (keep at least the most recent exchange)
            removed = self.conversation_history.pop(0)
            current_length -= len(removed)
    
    def generate_story(self, story_data, feedback="", previous_chapter=""):
        """
        Generate a story based on the provided data and feedback, using conversation history
        """
        # Format main characters for better readability
        characters_text = "\n".join(
            f"- {char['name']}: {char['description']}" for char in story_data["main_characters"]
        )
        
        # If feedback is provided, treat it as a new human input
        if feedback:
            human_input = f"H: {feedback}"
            # Add human feedback to conversation history
            self.conversation_history.append(human_input)
        
        # Build conversation context from history
        # Trim history first to ensure we're within limits
        self._trim_history()
        conversation_context = "\n\n".join(self.conversation_history)
        
        # Prepare the input data
        input_data = {
            "title": story_data["title"],
            "genre": story_data["genre"],
            "main_characters": characters_text,
            "facts": story_data["introduction"]["facts"],
            "outcome": story_data["introduction"]["outcome"],
            "story_beginning": story_data["story_beginning"],
            "conversation_context": conversation_context,
            "previous_chapter": previous_chapter
        }
        
        # Generate the story
        response = self.chain.run(input_data)
        
        # Add LLM response to conversation history
        chatbot_response = f"ChatBot: {response}"
        self.conversation_history.append(chatbot_response)
        
        # Trim history again after adding the new response
        self._trim_history()
        
        return response