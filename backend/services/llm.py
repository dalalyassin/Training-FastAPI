from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from schemas.chat import Prompt

client = AsyncOpenAI()


async def generate_stream_response(prompt: Prompt) -> AsyncIterator[str]:
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt.text}],
        temperature=0.7,
        stream=True,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield f"data: {delta.content}\n\n"
