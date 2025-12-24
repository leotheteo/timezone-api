from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from dateutil import parser
from zoneinfo import ZoneInfo
import re

app = FastAPI(title="Timezone API", docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

TZ_ALIASES = {
    "pst": "America/Los_Angeles",
    "pdt": "America/Los_Angeles",
    "est": "America/New_York",
    "edt": "America/New_York",
    "cst": "America/Chicago",
    "mst": "America/Denver",
    "gmt": "UTC",
    "utc": "UTC",
    "london": "Europe/London",
    "berlin": "Europe/Berlin",
    "tokyo": "Asia/Tokyo",
}

def normalize_timezone(input_tz: str):
    key = input_tz.strip().lower()
    return TZ_ALIASES.get(key, input_tz)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/docs", response_class=HTMLResponse)
def docs(request: Request):
    return templates.TemplateResponse("docs.html", {"request": request})

@app.post("/api/normalize")
def normalize(tz: str):
    return {"input": tz, "normalized": normalize_timezone(tz)}

@app.post("/api/when")
def when_is_it_for_me(text: str, timezone: str = "UTC"):
    tz = normalize_timezone(timezone)
    dt = parser.parse(text, fuzzy=True)
    localized = dt.replace(tzinfo=ZoneInfo(tz))
    local = localized.astimezone()
    return {
        "parsed": localized.isoformat(),
        "your_time": local.isoformat(),
        "timezone": str(local.tzinfo)
    }
