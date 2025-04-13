STORY_TEMPLATE = """
You are an AI story writer. Your task is to continue writing a story based on the information provided and previous conversation.

# Story Information
- Title: {title}
- Genre: {genre}

## Main Characters
{main_characters}

## Setting and Background
{facts}

## Historical Outcome
{outcome}

## Story Beginning
{story_beginning}

## Previous Chapter
{previous_chapter}

# Previous Conversation
{conversation_context}


Please generate the next scene in this story, taking into account the user's feedback and maintaining consistency with the previous chapter.
Focus on character development and ensure the story flows naturally from the previous events.
Keep the tone consistent with the genre and maintain the established character personalities.
Once you are done, I will review the result and will ask you to refine the current chapter or move to the next one. 
Give a title to the scene but DO NOT include the chapter number.
""" 