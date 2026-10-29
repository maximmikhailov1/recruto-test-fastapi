import secrets

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")

LOGIN = (
    '<form method="post" action="/auth/login">'
    '<input name="username"><input name="password" type="password">'
    "<button>OK</button></form>"
)


def code() -> str:
    return f"{secrets.randbelow(10000):04d}"


@app.get("/")
def public():
    return HTMLResponse(f"<h1>{code()}</h1>")


@app.get("/auth/")
def login_page():
    return HTMLResponse(LOGIN)


@app.post("/auth/login")
def login(request: Request, username: str = Form(), password: str = Form()):
    if username != "admin" or password != "admin":
        return HTMLResponse(LOGIN + "<p>fail</p>", status_code=401)
    request.session["ok"] = True
    return RedirectResponse("/auth/code", status_code=303)


@app.get("/auth/code")
def auth_code(request: Request):
    if not request.session.pop("ok", None):
        return RedirectResponse("/auth/", status_code=303)
    return HTMLResponse(f"<h1>{code()}</h1>")
