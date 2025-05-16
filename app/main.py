import os
import traceback
import logging

import click
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uvicorn.config import Config
from uvicorn.server import Server

from app.middleware.otel import setup_otel
from app.middleware.logging import LogMiddleware

# user
from app.routers.user import user
from app.routers.user import password

# company
from app.routers.company import company
from app.routers.company import roles
from app.utils.config.loader import ConfigLoader
from app.utils.config.logging import logger


def create_app() -> FastAPI:
    loader = ConfigLoader()
    configs = loader.get_config()

    cor_origins = configs.get("cor_origins", {})
    cor_origins_allowed = cor_origins.get("allowed", ["*"])
    cor_origins_blocked = cor_origins.get("blocked", [])
    origins = [
        origin for origin in cor_origins_allowed if origin not in cor_origins_blocked
    ]

    app = FastAPI()

    # setup_otel(app)
    app.add_middleware(LogMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def app_error_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": {
                    "message": "An error occurred, please try again.",
                    "error": str(exc),
                    # "location": f"{tb_frame.filename}:{tb_frame.lineno} in {tb_frame.name}()",
                },
            },
        )

    app.include_router(user.router)
    app.include_router(password.router)
    app.include_router(company.router)
    app.include_router(roles.router)

    @app.get("/")
    async def root():
        from opentelemetry import trace

        with trace.get_tracer(__name__).start_as_current_span("manual-span"):
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ok",
                    "version": configs.get("version"),
                    "name": configs.get("name"),
                    "description": configs.get("description"),
                    "repository": configs.get("repository"),
                    "documentation": configs.get("documentation"),
                    "message": "Welcome to the Userverse backend API",
                },
            )

    return app


@click.command()
@click.option("--port", default=8500, type=int, help="Port to run the server on.")
@click.option("--host", default="0.0.0.0", type=str, help="Host to run the server on.")
@click.option(
    "--env",
    default="development",
    type=click.Choice(["development", "production", "testing"]),
    help="Environment to run the server in.",
)
@click.option("--reload", is_flag=True, help="Reload the server on code change.")
@click.option(
    "--workers",
    default=1,
    type=int,
    help="Number of Uvicorn worker processes (ignored in reload mode).",
)
@click.option(
    "--json_config_path",
    default=None,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to a custom JSON configuration file.",
)
def main(
    port: int,
    host: str,
    env: str,
    reload: bool,
    workers: int,
    json_config_path: str | None,
):
    os.environ["ENV"] = env
    if json_config_path:
        os.environ["JSON_CONFIG_PATH"] = json_config_path

    if reload and workers > 1:
        os.environ["WATCHFILES_IGNORE"] = "*.pyc;.venv"
        logger.warning(
            "Reload mode does not support multiple workers. Using a single worker."
        )
        workers = 1

    logger.info(f"🚀 Starting Userverse API on http://{host}:{port} [env={env}]")

    # Silence all Uvicorn-related logs
    logging.getLogger("uvicorn").setLevel(logging.CRITICAL)
    logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)
    logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)

    if reload:
        uvicorn.run(
            "app.main:create_app",
            factory=True,
            host=host,
            port=port,
            reload=True,
            log_level="critical",
        )
    else:
        config = Config(
            app="app.main:create_app",
            factory=True,
            host=host,
            port=port,
            workers=workers,
            use_colors=False,
            log_level="critical",
        )
        server = Server(config)
        server.run()


if __name__ == "__main__":
    main()
