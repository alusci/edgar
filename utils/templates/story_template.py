STORY_TEMPLATE = """You are a creative writing assistant specialized in fiction writing.
Given the following story elements, generate an engaging scene or chapter.

Title: {title}
Genre: {genre}

Main Characters:
{main_characters}

Background Facts:
{facts}

Known Outcome:
{outcome}

Story So Far:
{previous_chapter}

User Feedback:
{feedback}

Current Scene:
{story_beginning}

Please generate the next scene in this story, taking into account the user's feedback and maintaining consistency with the previous chapter.
Focus on character development and ensure the story flows naturally from the previous events.
Keep the tone consistent with the genre and maintain the established character personalities.
Once you are done, I will review the result and will ask you to refine the current chapter or move to the next one. 
Give a title to the scene but DO NOT include the chapter number.
""" 