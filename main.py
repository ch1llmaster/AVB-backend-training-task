import asyncio

import uvicorn
from fastapi import FastAPI

from database.db_async import init_tables

app = FastAPI()


@app.get("/")
async def get_helo():
    return "Hello!"


if __name__ == "__main__":
    asyncio.run(init_tables())
    uvicorn.run(app)
