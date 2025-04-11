import json
import os

# Import the ChatApplication from utils
from utils.story_generator import ChatApplication

def main():
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


if __name__ == "__main__":
    main()
