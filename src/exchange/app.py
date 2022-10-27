import logging

from exchange.containers import Application
from exchange.settings import Settings
from exchange import api

logger = logging.getLogger(__name__)


def init_application() -> Application:
    app = Application()
    app.config.from_pydantic(Settings())
    app.init_resources()
    app.wire(packages=(api,))

    return app
