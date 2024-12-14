import asyncio

import openai

from app.arxiv import Paper


PROMPT = "与えられた文章を日本語に翻訳してください。[a math expression 0] のような表記はそのままにしてください。"


async def translate_paper(
    paper: Paper,
    api_key: str,
    base_url: str | None = None,
    model_name: str = "gpt-4o-mini",
) -> Paper:
    texts = [paper.title] + paper.texts

    client = openai.AsyncClient(api_key=api_key, base_url=base_url)
    
    requests = []
    for text in texts:
        requests.append(client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": text},
            ]
        ))

    responses = await asyncio.gather(*requests)
    translated_texts = [resp.choices[0].message.content for resp in responses]

    return Paper(
        title=translated_texts[0],
        texts=translated_texts[1:],
        tags=paper.tags,
        math_exprs=paper.math_exprs,
    )
