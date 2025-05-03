from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.configs import ConfigLoader
from app.middleware.logging import LogRouteMiddleware
from app.routers.user import user
from app.routers.user import password
from app.utils.app_error import AppError

import os
import click
import uvicorn


def create_app() -> FastAPI:

    json_config_path = os.getenv("JSON_CONFIG_PATH", None)
    # load configs
    loader = ConfigLoader(
        json_config_path=json_config_path,
    )
    configs = loader.get_config()

    cor_origins = configs.get("cor_origins", {})
    cor_origins_allowed = cor_origins.get("allowed", ["*"])
    cor_origins_blocked = cor_origins.get("blocked", [])
    origins = [
        origin for origin in cor_origins_allowed if origin not in cor_origins_blocked
    ]

    app = FastAPI()
    app.add_middleware(LogRouteMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def app_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "details": {
                    "message": "An error occurred, please try again.",
                    "error": str(exc) + ", path:" + str(request.scope.get("path")),
                },
            },
        )

    app.include_router(user.router)
    app.include_router(password.router)

    @app.get("/")
    async def root():
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
@click.option(
    "--reload",
    is_flag=True,
    help="Reload the server on code change (for development only).",
)
@click.option(
    "--workers",
    default=1,
    type=int,
    help="Number of Uvicorn worker processes (ignored in reload mode).",
)
@click.option(
    "--config",
    "json_config_path",
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
    """
    Main entry point for the FastAPI application.
    """
    from app.utils.config_logging import setup_logging

    setup_logging()

    # Export env for use inside create_app()
    os.environ["ENV"] = env
    if json_config_path:
        os.environ["JSON_CONFIG_PATH"] = json_config_path

    # Validation note: reload mode doesn't support workers > 1
    if reload and workers > 1:
        click.echo(
            "⚠️ Reload mode does not support multiple workers. Ignoring --workers."
        )
        workers = 1

    # Launch using factory to ensure consistent app creation
    click.echo(f"🚀 Starting Userverse API on http://{host}:{port} [env={env}]")
    uvicorn.run(
        "app.main:create_app",
        factory=True,
        host=host,
        port=port,
        reload=reload,
        workers=workers,
    )


if __name__ == "__main__":
    main()
