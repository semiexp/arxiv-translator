import hashlib
import json
import os
from typing import NamedTuple

from app.arxiv import Paper, load_from_arxiv
from app.translate import translate_paper


class AppConfig(NamedTuple):
    api_key: str
    base_url: str | None = None
    model_name: str = "gpt-4o-mini"
    cache_dir: str = "cache"


ARXIV_HTML_PREFIX = "https://arxiv.org/html/"
ARXIV_ABS_PREFIX = "https://arxiv.org/abs/"


class TranslationAppManager:
    def __init__(self, config: AppConfig):
        self.config = config
        os.makedirs(self.config.cache_dir, exist_ok=True)

    def normalize_url(self, paper_url: str) -> str:
        if paper_url.startswith(ARXIV_ABS_PREFIX):
            return ARXIV_HTML_PREFIX + paper_url[len(ARXIV_ABS_PREFIX) :]
        elif paper_url.startswith(ARXIV_HTML_PREFIX):
            return paper_url
        else:
            raise ValueError(f"Invalid URL: {paper_url}")

    def get_cache_path(self, paper_url: str) -> str:
        return os.path.join(self.config.cache_dir, hashlib.md5(paper_url.encode()).hexdigest() + ".json")

    async def get_paper(self, paper_url: str) -> tuple[Paper, Paper]:
        cache_path = self.get_cache_path(paper_url)
        if os.path.exists(cache_path):
            with open(cache_path) as f:
                data = json.load(f)

            original = Paper.from_dict(data["original"])
            translated = Paper.from_dict(data["translated"])
            return original, translated

        original = load_from_arxiv(paper_url)
        translated = await translate_paper(
            original,
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            model_name=self.config.model_name,
        )

        with open(cache_path, "w") as f:
            json.dump(
                {
                    "url": paper_url,
                    "original": original.to_dict(),
                    "translated": translated.to_dict(),
                },
                f,
            )

        return original, translated

    async def get_markdown(self, paper_url: str) -> str:
        paper_url = self.normalize_url(paper_url)
        original, translated = await self.get_paper(paper_url)

        res = [f"# {original.title}"]

        for i in range(len(original.texts)):
            tag = original.tags[i]
            text = original.restore_math_expr(original.texts[i])
            translated_text = translated.restore_math_expr(translated.texts[i])

            if tag == "p":
                res.append(text)
                res.append(translated_text)
                continue

            if tag == "h1":
                prefix = "##"
            elif tag == "h2":
                prefix = "###"
            else:
                prefix = "####"

            res.append(f"{prefix} {text} / {translated_text}")

        return "\n\n".join(res)

    def get_paper_list(self) -> list[dict]:
        res = []
        for file in os.listdir(self.config.cache_dir):
            if not file.endswith(".json"):
                continue

            with open(os.path.join(self.config.cache_dir, file)) as f:
                data = json.load(f)

            url = data["url"]
            title = data["original"]["title"]

            res.append({
                "url": url,
                "title": title,
            })

        return res
