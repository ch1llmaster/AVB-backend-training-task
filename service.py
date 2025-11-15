import asyncio

import httpx

BASE_URL = "http://127.0.0.1:8000/"


async def test_shortener():
    async with httpx.AsyncClient() as client:
        urls_to_shorten = [
            "https://learn.javascript.ru/code-editors",
            "https://stackoverflow.com/questions/79820472/pyinstaller-it-doesnt-generate-an-exe-file",
            "https://github.com/fastapi/fastapi",
        ]

        for url in urls_to_shorten:
            response = await client.post(BASE_URL, json={"url": url})
            print("POST Response:", response.status_code, response.json())


if __name__ == "__main__":
    asyncio.run(test_shortener())
