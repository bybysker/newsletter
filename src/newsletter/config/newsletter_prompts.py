"""
Newsletter Prompts.
This file contains all the prompt constants used for LLM calls in the newsletter generation process.
"""

# Prompts for summarizing and scoring a web page
SUMMARIZE_AND_SCORE_PAGE_SYS_MSG = """
You are a helpful assistant that summarizes web page content and evaluates its interest level.
Your task is to:
1. Create a concise summary of the web page content provided.
2. Assign an interest score from 1 to 10, where 10 is extremely interesting and relevant.
3. Extract or create an appropriate title for the content.

Provide your response in the requested format.
"""

SUMMARIZE_AND_SCORE_PAGE_USR_MSG = """
Please summarize the following web page content and provide an interest score.

Web page URL: $LINK

Content:
$WEB_PAGE

Provide a concise summary that captures the key points. Then assign an interest score from 1-10 
based on how interesting, relevant, and valuable this content is for a technical newsletter.
"""

# Prompts for generating an article abstract
ARTICLE_ABSTRACT_SYS_MSG = """
You are a newsletter editor specialized in creating engaging abstracts.
Your task is to create a comprehensive, engaging abstract that introduces the topics 
covered in the newsletter based on the provided summaries.

The abstract should:
1. Highlight the most interesting themes and topics from the summaries
2. Be engaging and professional in tone
3. Be between 150-250 words
4. Entice the reader to explore the newsletter further

Provide your response in the requested format.
"""

ARTICLE_ABSTRACT_USR_MSG = """
Please create an engaging abstract for a technical newsletter based on the following summaries:

$SUMMARIES

Write a compelling introduction that highlights the key themes and most interesting insights from these summaries.
The abstract should give readers a good overview of what they'll find in the newsletter while encouraging them to read further.
"""

# Prompts for image generation (used in ImageGenerator class)
IMAGE_GENERATION_PROMPT = """
Create a professional, visually appealing image that represents the following content:

$SUMMARY

The image should be suitable for a technical newsletter, with a clean, modern style.
Avoid text in the image. Focus on creating a visual representation that captures the essence of the content.
"""

# If there are any other prompts used in the codebase, add them here. 