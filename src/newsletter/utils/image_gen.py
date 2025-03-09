import os
import asyncio
from openai import AsyncOpenAI
from pathlib import Path
import logging
from datetime import datetime
from dotenv import load_dotenv
import time
import aiohttp
import aiofiles
import base64
from io import BytesIO
from newsletter_prompts import IMAGE_GENERATION_PROMPT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Create output directory if it doesn't exist
        self.output_dir = Path('generated_images')
        self.output_dir.mkdir(exist_ok=True)

    async def generate_image(self, summary: str, size: str = "1024x1024", quality: str = "standard") -> dict:
        """
        Generate an image based on the provided summary.
        
        Args:
            summary (str): Text description for image generation
            size (str): Image size (1024x1024, 1792x1024, or 1024x1792)
            quality (str): Image quality ("standard" or "hd")
            
        Returns:
            dict: Dictionary containing the image URL, local path, and base64-encoded PNG
        """
        try:
            logger.info(f"Generating image for summary: {summary}")
            
            # Create prompt using the template
            image_prompt = IMAGE_GENERATION_PROMPT.replace("$SUMMARY", summary)
            
            # Generate image using DALL-E 3
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size=size,
                quality=quality,
                n=1
            )

            # Get image URL
            image_url = response.data[0].url
            
            # Generate unique filename based on timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = self.output_dir / f"generated_image_{timestamp}.png"
            
            # Download the image
            logger.info(f"Downloading image from {image_url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    image_content = await response.read()
            
            # Save the image locally
            async with aiofiles.open(image_path, 'wb') as f:
                await f.write(image_content)
                
            # Convert the image to base64
            base64_image = base64.b64encode(image_content).decode('utf-8')
            
            logger.info(f"Image generated and downloaded successfully.")
            
            return {
                "url": image_url,
                "local_path": str(image_path),
                "timestamp": timestamp,
                "base64_png": base64_image
            }
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise

async def main():
    # Example usage
    generator = ImageGenerator()
    
    # Example summary
    summary = "A serene mountain landscape at sunset with snow-capped peaks reflected in a crystal-clear lake"
    
    try:
        result = await generator.generate_image(summary)
        print(f"Image generated successfully!")
        print(f"Image URL: {result['url']}")
        print(f"Local path: {result['local_path']}")
        print(f"Base64 PNG available (length: {len(result['base64_png'])} characters)")
        
    except Exception as e:
        print(f"Failed to generate image: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
