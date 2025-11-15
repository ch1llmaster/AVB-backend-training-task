from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl

from database.db_async import delete_tables, create_tables
from database.methods.url_base import create_new_record, get_record_by_uniq_id
from utils import generate_unique_id


@asynccontextmanager
async def lifespan(my_app: FastAPI):
    await delete_tables()
    print("drop all tables")
    await create_tables()
    print("create all tables")
    yield

ADDRESS = "http://127.0.0.1:8000"

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


class URLRequest(BaseModel):
    url: HttpUrl


@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("endpoints.html", {"request": request})


@app.post("/", status_code=201)
async def shortened_url(data: URLRequest):
    default_url = str(data.url)
    short_id = generate_unique_id()
    short_url = f"{ADDRESS}/{short_id}"
    await create_new_record(default_url=default_url,
                            uniq_id=short_id,
                            shortened_url=short_url)
    return {"short_id": short_id, "short_url": short_url}


@app.get("/{short_id}")
async def get_original_url(short_id: str):
    record = await get_record_by_uniq_id(uniq_id=short_id)
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")
    default_url = record.default_url
    return RedirectResponse(url=default_url, status_code=307)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
