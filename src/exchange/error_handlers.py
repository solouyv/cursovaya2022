from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

templates = Jinja2Templates(directory="templates")


def register_error_handler(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    def handle_all_errors(request: Request, error: Exception):
        return templates.TemplateResponse("main.html", {"request": request, "errors": ["Something went wrong"]})
