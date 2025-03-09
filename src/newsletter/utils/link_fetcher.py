import aiohttp
import asyncio
from typing import List 
from html2text import HTML2Text

class LinkFetcher:
    def __init__(self, links: List[str]):
        self.links = links   

    async def fetch_page(self, session, link):
      """Fetch a single page asynchronously"""
      h2t = HTML2Text()
      h2t.ignore_links = True
      h2t.ignore_images = True
      h2t.ignore_tables = True
      try:
          async with session.get(link, ssl=False) as response:
              html = await response.text()
              return h2t.handle(html)
      except Exception as e:
          print(f"Error fetching {link}: {str(e)}")
          return None

    async def fetch_all_pages(self):
        """Fetch all pages concurrently"""
        new_pages = {}
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_page(session, link) for link in self.links]
            results = await asyncio.gather(*tasks)
            
            # Create dictionary of results
            for link, content in zip(self.links, results):
                if content:  # Only add if content was successfully fetched
                    new_pages[link] = content
        
        return new_pages