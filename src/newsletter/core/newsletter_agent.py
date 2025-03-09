import time
import asyncio
from typing import List, Dict, Tuple, Optional
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import AsyncOpenAI
from newsletter.utils.image_gen import ImageGenerator
from newsletter.utils.link_fetcher import LinkFetcher
from newsletter.config.newsletter_prompts import (
    SUMMARIZE_AND_SCORE_PAGE_SYS_MSG,
    SUMMARIZE_AND_SCORE_PAGE_USR_MSG,
    ARTICLE_ABSTRACT_SYS_MSG,
    ARTICLE_ABSTRACT_USR_MSG
)

from rich import print
from pydantic import BaseModel


class PageSummary(BaseModel):
    link: str
    title: str
    content_summary: str
    interest_score: float
    image: Optional[str] = None

class Newsletter(BaseModel):
    full_newsletter: str
    links: List[str]

class ArticleAbstract(BaseModel):
    abstract: str

class NewsletterAgent:
    def __init__(self, client: AsyncOpenAI, links: List[str], max_summaries: int = 8):
        self.client = client
        self.links = links
        self.logger = logging.getLogger(__name__)
        self.pages_summaries: List[PageSummary] = []
        self.max_summaries = max_summaries

    async def fetch_related_web_pages(self) -> List[str]:
        start_time = time.time()
        self.logger.info("Starting web page fetching")

        web_pages = await LinkFetcher(self.links).fetch_all_pages()
        
        execution_time = time.time() - start_time
        self.logger.info(f"Web page fetching completed in {execution_time:.2f} seconds. Found {len(web_pages)} pages")
        
        return web_pages
    
    async def summarize_and_score_page(self, link: str, page_content: str) -> PageSummary:
        """Summarize a single page asynchronously."""
        start_time = time.time()
        self.logger.info(f"Starting page summarization for link: {link}")
        
        try:
            completion = await self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SUMMARIZE_AND_SCORE_PAGE_SYS_MSG},
                    {"role": "user", "content": SUMMARIZE_AND_SCORE_PAGE_USR_MSG
                                                                            .replace("$WEB_PAGE", page_content)
                                                                            .replace("$LINK", link)}
                ],
                response_format=PageSummary
            )
            execution_time = time.time() - start_time
            self.logger.info(f"Page summarization completed in {execution_time:.2f} seconds for link: {link}")

            return completion.choices[0].message.parsed
        except Exception as e:
            self.logger.error(f"Error summarizing page {link}: {str(e)}")
            return PageSummary(link=link, title=f"Error summarizing page: {str(e)}", content_summary=f"Error summarizing page: {str(e)}", interest_score=4)

    async def summarize_and_score_all_pages(self) -> List[PageSummary]:
        """Process all pages in parallel using asyncio.gather."""
        start_time = time.time()
        self.logger.info("Starting summarization of all pages")
        
        pages = await self.fetch_related_web_pages()
        # Create tasks for all pages
        tasks = [
            self.summarize_and_score_page(link, content)
            for link, content in pages.items()
        ]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)

        execution_time = time.time() - start_time
        self.logger.info(f"All pages summarization completed in {execution_time:.2f} seconds. Processed {len(results)} pages")
        
        return results

    async def generate_article_abstract(self) -> ArticleAbstract:
        """Generate article abstract based on top N summaries and rankings."""
        start_time = time.time()

        # Sort summaries by interest score
        sorted_summaries = sorted(self.pages_summaries, key=lambda x: x.interest_score, reverse=True)
        top_summaries = sorted_summaries[:self.max_summaries]
        
        # Combine selected summaries into one context, including rankings
        combined_summaries = "\n".join(
            f"Summary from {summary.link}:\n{summary.content_summary}"
            for summary in top_summaries
        )
        
        try:
            completion = await self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": ARTICLE_ABSTRACT_SYS_MSG},
                    {"role": "user", "content": ARTICLE_ABSTRACT_USR_MSG.replace("$SUMMARIES", combined_summaries)}
                ],
                response_format=ArticleAbstract
            )
            
            article_abstract = completion.choices[0].message.parsed
            execution_time = time.time() - start_time
            self.logger.info(f"Article abstract generation completed in {execution_time:.2f} seconds")
            
            return article_abstract
        
        except Exception as e:
            self.logger.error(f"Error generating article abstract: {str(e)}")
            return ArticleAbstract(
                abstract=f"Error generating article abstract: {str(e)}"
            )

    async def compose_full_newsletter(self) -> Newsletter:
        """Compose the full newsletter in HTML format with abstract, summaries, and other links."""
        try:
            start_time = time.time()
            self.logger.info("Starting newsletter composition")
            
            # Import the HTML templates
            from newsletter.templates.newsletter_templates import (
                HTML_HEAD, 
                ABSTRACT_SECTION, 
                SUMMARY_SECTION, 
                OTHER_NEWS_START, 
                OTHER_NEWS_LINK, 
                OTHER_NEWS_END, 
                HTML_FOOTER
            )
            
            # If page summaries are not already populated, generate them
            if not self.pages_summaries:
                self.pages_summaries = await self.summarize_and_score_all_pages()

            # Generate article abstract if not already generated
            article_abstract = await self.generate_article_abstract()
            
            # Sort summaries by interest score
            sorted_summaries = sorted(self.pages_summaries, key=lambda x: x.interest_score, reverse=True)
            
            # Get top summaries for detailed inclusion
            top_summaries = sorted_summaries[:self.max_summaries]

            # Gennerate summaries images
            for summary in top_summaries:
                summary.image = await ImageGenerator().generate_image(summary.content_summary)
            
            # Get remaining links for the "Other news" section
            other_links = [summary.link for summary in sorted_summaries[self.max_summaries:]]
            
            # Start building HTML content
            html_content = HTML_HEAD
            
            # Add abstract section
            html_content += ABSTRACT_SECTION.format(abstract=article_abstract.abstract)
            
            # Add each summary
            for summary in top_summaries:
                html_content += SUMMARY_SECTION.format(
                    title=summary.title,
                    content=summary.content_summary,
                    link=summary.link
                )
            
            # Add "Other news" section
            if other_links:
                html_content += OTHER_NEWS_START
                
                for link in other_links:
                    html_content += OTHER_NEWS_LINK.format(link=link)
                
                html_content += OTHER_NEWS_END
            
            # Add HTML footer
            html_content += HTML_FOOTER
            
            # Get all links for the Newsletter object
            all_links = [summary.link for summary in sorted_summaries]
            
            execution_time = time.time() - start_time
            self.logger.info(f"Newsletter composition completed in {execution_time:.2f} seconds")
            
            return Newsletter(
                full_newsletter=html_content,
                links=all_links
            )
        
        except Exception as e:
            self.logger.error(f"Error composing newsletter: {str(e)}")
            return Newsletter(
                full_newsletter=f"<p>Error composing newsletter: {str(e)}</p>",
                links=self.links
            )

    async def run_agent(self):
        """Execute the full newsletter generation pipeline."""
        try:
            start_time = time.time()
            self.logger.info("Starting newsletter agent execution")
            
            # Step 1: Generate page summaries
            self.pages_summaries = await self.summarize_and_score_all_pages()
            
            # Step 2: Compose the full newsletter
            full_newsletter = await self.compose_full_newsletter()
            
            execution_time = time.time() - start_time
            self.logger.info(f"Newsletter agent execution completed in {execution_time:.2f} seconds")
            
            return full_newsletter
        
        except Exception as e:
            self.logger.error(f"Error in newsletter agent execution: {str(e)}")
            return Newsletter(
                full_newsletter=f"<p>Error generating newsletter: {str(e)}</p>",
                links=self.links
            ) 