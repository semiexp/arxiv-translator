import argparse
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.app_manager import AppConfig, TranslationAppManager

config: AppConfig | None = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"response": "hello"}


class MarkdownRequest(BaseModel):
    arxiv_url: str


@app.post("/markdown")
async def translate_to_markdown(request: MarkdownRequest):
    manager = TranslationAppManager(config)

    markdown = await manager.get_markdown(request.arxiv_url)
    return {"response": markdown}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8090)
    parser.add_argument("--api-key", type=str, default=".secret/apikey.txt")
    parser.add_argument("--base-url", type=str, default=None)
    parser.add_argument("--model-name", type=str, default="gpt-4o-mini")
    parser.add_argument("--cache-dir", type=str, default=".cache")
    args = parser.parse_args()

    with open(args.api_key) as f:
        api_key = f.read().strip()

    global config
    config = AppConfig(
        api_key=api_key,
        base_url=args.base_url,
        model_name=args.model_name,
        cache_dir=args.cache_dir,
    )

    uvicorn.run(app, port=args.port)


if __name__ == "__main__":
    main()
