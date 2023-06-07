import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from exchange import api, constants
from exchange.app import init_application
from exchange.containers import Application
from exchange.error_handlers import register_error_handler

templates = Jinja2Templates(directory="templates")


def create_api() -> FastAPI:
    app: Application = init_application()

    api_app = FastAPI(
        title=constants.PROJECT_NAME,
        version=app.config.version(),
        docs_url=f"{constants.API_PREFIX}{constants.SWAGGER_DOC_URL}",
        description=constants.DESCRIPTION,
        openapi_url=f"{constants.API_PREFIX}/openapi.json",
    )
    api_app.include_router(api.router, prefix="")
    api_app.app = app
    api_app.mount("/static", StaticFiles(directory="static"), name="static")

    register_error_handler(api_app)

    return api_app


def run_api():
    options = {
        "host": "0.0.0.0",  # noqa: S104
        "port": 8000,
        "log_level": "debug",
        "reload": os.getenv("ENV", "prod") == "development",
    }

    uvicorn.run("exchange.api_app:create_api", **options)
