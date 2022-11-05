import logging

from exchange import api
from exchange.containers import Application
from exchange.settings import Settings

logger = logging.getLogger(__name__)


def init_application() -> Application:
    app = Application()
    app.config.from_pydantic(Settings())
    app.init_resources()
    app.wire(packages=(api,))

    return app
