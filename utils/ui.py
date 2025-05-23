import json
import os
import gradio as gr
from utils.story_generator import ChatApplication


class StoryGeneratorUI:
    def __init__(self):
        self.app = ChatApplication()
        self.story_data = None
        self.story_context = []
        self.chapter_number = 1
        self.current_chapter = ""

    def create_story_data(self, title, genre, facts, outcome, story_beginning, characters_json):
        try:
            # Try to parse characters JSON input
            main_characters = json.loads(characters_json)
            
            # Create story data structure
            self.story_data = {
                "title": title,
                "genre": genre,
                "main_characters": main_characters,
                "introduction": {
                    "facts": facts,
                    "site_note": "",
                    "outcome": outcome
                },
                "story_beginning": story_beginning
            }
            
            self.story_context = []
            self.chapter_number = 1
            self.current_chapter = ""
            
            return f"Story data created: {self.story_data['title']}", None
        except Exception as e:
            return f"Error creating story data: {str(e)}", None


    def generate_chapter(self, feedback=""):
        if self.story_data is None:
            return "Please create story data first", None
        
        try:
            # Get the previous chapter from the story context
            previous_chapter = self.story_context[-1] if self.story_context else ""
            
            # Generate the chapter using the feedback and conversation history
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
            return "No chapter to accept", None, ""
        
        self.story_context.append(self.current_chapter)
        self.chapter_number += 1
        prev_chapter = self.current_chapter
        self.current_chapter = ""
        
        return f"Chapter accepted. Ready to generate Chapter {self.chapter_number}", None, ""


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
        
        # Also save the story data as JSON
        data_file = f"data/inputs/{file_name}.json"
        with open(data_file, "w") as f:
            json.dump(self.story_data, f, indent=4)
            
        return f"Story saved to {output_file} and data saved to {data_file}", None


    def download_story(self, file_name):
        """Create downloadable story files for the user"""
        if not self.story_context:
            return "No story to download", None, None
        
        if not file_name:
            file_name = self.story_data['title'].lower().replace(' ', '_')
        
        # Create story content
        story_content = f"# {self.story_data['title']}\n\n"
        for i, chapter in enumerate(self.story_context, 1):
            story_content += f"\n## Chapter {i}\n\n"
            story_content += chapter
            story_content += "\n\n"
        
        # Create JSON content
        json_content = json.dumps(self.story_data, indent=4)
        
        # Create temporary directory and files with proper names
        import tempfile
        import os
        
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Create files with proper names
        text_file_path = os.path.join(temp_dir, f"{file_name}.txt")
        json_file_path = os.path.join(temp_dir, f"{file_name}.json")
        
        # Write story content to text file
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(story_content)
        
        # Write JSON content to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_content)
    
        # Return both files for download
        return f"Story '{self.story_data['title']}' is ready for download", text_file_path, json_file_path


    def load_example_data(self):
        with open("data/inputs/stone_giant_heroons.json", "r") as f:
            example_data = json.load(f)
            
        characters_json = json.dumps(example_data["main_characters"], indent=2)
        
        return (
            example_data["title"],
            example_data["genre"],
            example_data["introduction"]["facts"],
            example_data["introduction"]["outcome"],
            example_data["story_beginning"],
            characters_json
        )


def ui_main():
    ui = StoryGeneratorUI()
    
    with gr.Blocks(title="EDGAR - Story Generator") as demo:
        gr.Markdown("# EDGAR - AI Story Generator")
        
        with gr.Tabs():
            with gr.TabItem("1. Story Setup"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Basic Story Information")
                        title_input = gr.Textbox(label="Title", placeholder="Enter story title")
                        genre_input = gr.Textbox(label="Genre", placeholder="Enter story genre")
                        
                        gr.Markdown("### Introduction")
                        facts_input = gr.Textbox(
                            label="Historical Facts", 
                            placeholder="Enter historical facts about the setting",
                            lines=5
                        )
                        outcome_input = gr.Textbox(
                            label="Historical Outcome", 
                            placeholder="Enter how the historical events ended",
                            lines=5
                        )
                        
                        story_beginning_input = gr.Textbox(
                            label="Story Beginning", 
                            placeholder="Enter how your story begins",
                            lines=5
                        )
                        
                    with gr.Column(scale=1):
                        gr.Markdown("### Main Characters")
                        gr.Markdown("""
                        Enter characters in JSON format:
                        ```json
                        [
                          {"name": "Character1", "description": "Description1"},
                          {"name": "Character2", "description": "Description2"}
                        ]
                        ```
                        """)
                        characters_input = gr.Code(
                            label="Characters JSON",
                            language="json",
                            lines=20,
                            value="[]"
                        )
                        
                        load_example_btn = gr.Button("Load Example Data")
                        create_btn = gr.Button("Create Story Data")
                        status = gr.Textbox(label="Status", interactive=False)
                
            with gr.TabItem("2. Story Generation"):
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Group():
                            gr.Markdown("### Generation Controls")
                            feedback_input = gr.Textbox(
                                label="Feedback for regeneration (optional)",
                                placeholder="Enter feedback to guide the story generation",
                                lines=3
                            )
                            generate_btn = gr.Button("Generate Chapter")
                            accept_btn = gr.Button("Accept Chapter & Continue")
                        
                        with gr.Group():
                            gr.Markdown("### Download Story")
                            file_name_input = gr.Textbox(
                                label="File Name (optional)",
                                placeholder="Enter a file name for the story (without extension)"
                            )
                            download_btn = gr.Button("Download Story")
                            story_file = gr.File(label="Story Text (click to download)", visible=False, interactive=True)
                            data_file = gr.File(label="Story Data JSON (click to download)", visible=False, interactive=True)
                    
                    with gr.Column(scale=2):
                        generation_status = gr.Textbox(label="Generation Status", interactive=False)
                        chapter_output = gr.Markdown(
                            value="Generated chapter will appear here. Start by creating story data."
                        )
        
        # Event handlers
        load_example_btn.click(
            fn=ui.load_example_data, 
            inputs=[], 
            outputs=[title_input, genre_input, facts_input, outcome_input, story_beginning_input, characters_input]
        )
        
        create_btn.click(
            fn=ui.create_story_data, 
            inputs=[title_input, genre_input, facts_input, outcome_input, story_beginning_input, characters_input],
            outputs=[status, chapter_output]
        )
        
        generate_btn.click(
            fn=ui.generate_chapter, 
            inputs=[feedback_input], 
            outputs=[generation_status, chapter_output]
        )
        
        accept_btn.click(
            fn=ui.accept_chapter, 
            inputs=[], 
            outputs=[generation_status, chapter_output, feedback_input]
        )
        
        download_btn.click(
            fn=ui.download_story,
            inputs=[file_name_input],
            outputs=[generation_status, story_file, data_file]
        ).then(
            fn=lambda: (gr.update(visible=True), gr.update(visible=True)),
            inputs=[],
            outputs=[story_file, data_file]
        )
    
    demo.launch(share=False)
