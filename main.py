import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import pyshorteners
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from database.db_async import delete_tables, create_tables
from database.methods.url_base import create_new_record, get_record_by_id

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(my_app: FastAPI):
    await delete_tables()
    print("drop all tables")
    await create_tables()
    print("create all tables")
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

pys = pyshorteners.Shortener()


class URLRequest(BaseModel):
    url: HttpUrl


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("endpoints.html", {"request": request})


@app.post("/", status_code=201)
async def shortened_url(data: URLRequest):
    default_url = str(data.url)
    short_url = pys.tinyurl.short(default_url)
    record = await create_new_record(default_url, short_url)
    return {"short_id": record.id, "short_url": short_url}


@app.get("/{short_id}")
async def get_default_url(short_id: int):
    record = await get_record_by_id(short_id)
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")
    default_url = record.default_url
    return RedirectResponse(url=default_url, status_code=307)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
