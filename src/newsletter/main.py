import os
import uvicorn
from fastapi import FastAPI
from openai import AsyncOpenAI
from newsletter.core.newsletter_agent import NewsletterAgent
from pydantic import BaseModel
from typing import List

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()

class NewsletterRequest(BaseModel):
    links: List[str]

@app.post("/generate-newsletter")
async def generate_newsletter(request: NewsletterRequest):
    data = request.model_dump_json()
    print(data)

    agent = NewsletterAgent(client, request.links)
    newsletter = await agent.compose_full_newsletter()

    return {"newsletter": newsletter.full_newsletter}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)