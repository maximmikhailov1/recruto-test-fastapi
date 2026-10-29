import os
import secrets
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

AUTH_USERNAME = os.environ["AUTH_USERNAME"]
AUTH_PASSWORD = os.environ["AUTH_PASSWORD"]

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET"],
)
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def code() -> str:
    return f"{secrets.randbelow(10000):04d}"


@app.get("/")
def public(request: Request):
    return templates.TemplateResponse(
        request, "code.html", {"code": code()}
    )


@app.get("/auth/")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@app.post("/auth/login")
def login(request: Request, username: str = Form(), password: str = Form()):
    if username != AUTH_USERNAME or password != AUTH_PASSWORD:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Неверный логин или пароль"},
            status_code=401,
        )
    request.session["ok"] = True
    return RedirectResponse("code", status_code=303)


@app.get("/auth/code")
def auth_code(request: Request):
    if not request.session.pop("ok", None):
        return RedirectResponse("../", status_code=303)
    return templates.TemplateResponse(
        request, "code.html", {"code": code()}
    )
