import json
import os
import argparse
import gradio as gr

# Import the ChatApplication from utils
from utils.story_generator import ChatApplication

def cli_main():
    # Load the story data
    with open("data/inputs/stone_giant_heroons.json", "r") as f:
        story_data = json.load(f)
    
    # Initialize the chat application
    app = ChatApplication()
    
    # Initialize story context
    story_context = []
    chapter_number = 1
    feedback = ""
    revision = False
    
    while True:
        print(f"\nGenerating Chapter {chapter_number}...")
        print("-" * 50)
        
        # Generate the next chapter
        previous_chapter = story_context[-1] if story_context else ""
        chapter = app.generate_story(story_data, feedback=feedback, previous_chapter=previous_chapter)

        # Display the generated chapter
        print(f"\nChapter {chapter_number}:")
        print("-" * 50)
        print(chapter)
        print("\n" + "-" * 50)
        
        # Get user feedback
        print("\nOptions:")
        print("1. Provide feedback and regenerate this chapter")
        print("2. Accept and continue to next chapter")
        print("*. Save and exit")
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "1":
            if revision:
                story_context.pop()
            feedback = input("\nPlease provide your feedback: ")
            story_context.append(chapter)
            revision = True

        elif choice == "2":
            if revision:
                feedback = ""
                story_context.pop()
                revision = False
            
            # Add chapter to context and continue
            story_context.append(chapter)
            chapter_number += 1
        else:
            # Add final chapter to context
            story_context.append(chapter)
            chapter_number += 1

            # Save the story to a file
            output_file = f"data/outputs/{story_data['title'].lower().replace(' ', '_')}.txt"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, "w") as f:
                f.write(f"# {story_data['title']}\n\n")
                for i, chapter in enumerate(story_context, 1):
                    f.write(f"\n## Chapter {i}\n\n")
                    f.write(chapter)
                    f.write("\n\n")
            
            print(f"\nStory saved to {output_file}")
            break


class StoryGeneratorUI:
    def __init__(self):
        self.app = ChatApplication()
        self.story_data = None
        self.story_context = []
        self.chapter_number = 1
        self.current_chapter = ""

    def load_story_data(self, file_obj):
        if file_obj is None:
            return "Please upload a JSON file", None
        
        try:
            # With newer Gradio versions, file_obj is the file path
            if isinstance(file_obj, str):
                with open(file_obj, 'r') as f:
                    self.story_data = json.load(f)
            else:
                # Try to handle it as a file-like object (older approach)
                try:
                    content = file_obj.read().decode('utf-8')
                    self.story_data = json.loads(content)
                except AttributeError:
                    # For newer Gradio versions that return file path as tempfile
                    with open(file_obj.name, 'r') as f:
                        self.story_data = json.load(f)
            
            self.story_context = []
            self.chapter_number = 1
            self.current_chapter = ""
            return f"Story data loaded: {self.story_data['title']}", None
        except Exception as e:
            return f"Error loading story data: {str(e)}", None

    def generate_chapter(self, feedback=""):
        if self.story_data is None:
            return "Please load story data first", None
        
        try:
            # Get the previous chapter from the story context
            previous_chapter = self.story_context[-1] if self.story_context else ""
            
            # Generate the chapter
            self.current_chapter = self.app.generate_story(
                self.story_data, 
                feedback=feedback,
                previous_chapter=previous_chapter
            )
            
            chapter_display = f"# Chapter {self.chapter_number}\n\n{self.current_chapter}"
            return f"Generated chapter {self.chapter_number}", chapter_display
        except Exception as e:
            return f"Error generating chapter: {str(e)}", None

    def accept_chapter(self):
        if not self.current_chapter:
            return "No chapter to accept", None, ""  # Return empty string as third return value to clear feedback
        
        self.story_context.append(self.current_chapter)
        self.chapter_number += 1
        prev_chapter = self.current_chapter
        self.current_chapter = ""
        
        return f"Chapter accepted. Ready to generate Chapter {self.chapter_number}", None, ""  # Return empty string to clear feedback

    def save_story(self, file_name):
        if not self.story_context:
            return "No story to save", None
        
        if not file_name:
            file_name = self.story_data['title'].lower().replace(' ', '_')
        
        output_file = f"data/outputs/{file_name}.txt"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w") as f:
            f.write(f"# {self.story_data['title']}\n\n")
            for i, chapter in enumerate(self.story_context, 1):
                f.write(f"\n## Chapter {i}\n\n")
                f.write(chapter)
                f.write("\n\n")
        
        return f"Story saved to {output_file}", None

def ui_main():
    ui = StoryGeneratorUI()
    
    with gr.Blocks(title="EDGAR - Story Generator") as demo:
        gr.Markdown("# EDGAR - AI Story Generator")
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input = gr.File(
                    label="1. Select Story Data (JSON)",
                    file_types=[".json"],
                    type="filepath"  # Explicitly set to return filepath
                )
                load_btn = gr.Button("Load Story Data")
                status = gr.Textbox(label="Status", interactive=False)
                
                with gr.Group():  # Changed from gr.Box() to gr.Group()
                    gr.Markdown("### Generation Controls")
                    feedback_input = gr.Textbox(
                        label="Feedback for regeneration (optional)",
                        placeholder="Enter feedback to guide the story generation",
                        lines=3
                    )
                    generate_btn = gr.Button("2. Generate Chapter")
                    accept_btn = gr.Button("3. Accept Chapter & Continue")
                
                with gr.Group():  # Changed from gr.Box() to gr.Group()
                    gr.Markdown("### Save Story")
                    file_name_input = gr.Textbox(
                        label="File Name (optional)",
                        placeholder="Enter a file name for the story (without extension)"
                    )
                    save_btn = gr.Button("4. Save Story")
            
            with gr.Column(scale=2):
                chapter_output = gr.Markdown(
                    value="Generated chapter will appear here. Start by loading a story data file."
                )
        
        # Event handlers
        load_btn.click(fn=ui.load_story_data, inputs=[file_input], outputs=[status, chapter_output])
        generate_btn.click(fn=ui.generate_chapter, inputs=[feedback_input], outputs=[status, chapter_output])
        accept_btn.click(fn=ui.accept_chapter, inputs=[], outputs=[status, chapter_output, feedback_input])  # Add feedback_input as output
        save_btn.click(fn=ui.save_story, inputs=[file_name_input], outputs=[status, chapter_output])
    
    demo.launch(share=False)

def main():
    parser = argparse.ArgumentParser(description="EDGAR - AI Story Generator")
    parser.add_argument("--ui", action="store_true", help="Launch the Gradio UI")
    args = parser.parse_args()
    
    if args.ui:
        ui_main()
    else:
        cli_main()

if __name__ == "__main__":
    main()
