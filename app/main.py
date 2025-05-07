import traceback
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.utils.config.loader import ConfigLoader
from app.utils.config.logging import logger
from app.middleware.logging import LogMiddleware
from app.routers.user import user
from app.routers.user import password

import os
import click
import uvicorn


def create_app() -> FastAPI:

    # load configs
    loader = ConfigLoader()
    configs = loader.get_config()

    cor_origins = configs.get("cor_origins", {})
    cor_origins_allowed = cor_origins.get("allowed", ["*"])
    cor_origins_blocked = cor_origins.get("blocked", [])
    origins = [
        origin for origin in cor_origins_allowed if origin not in cor_origins_blocked
    ]

    app = FastAPI()
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
        # Get traceback info as a list of frames
        tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
        tb_str = ''.join(tb_lines)

        # Extract the last call (where the exception occurred)
        tb_frame = traceback.extract_tb(exc.__traceback__)[-1]  # Last frame
        file_name = tb_frame.filename
        line_number = tb_frame.lineno
        func_name = tb_frame.name

        logger.error(
            f"Unhandled Exception in {file_name}, line {line_number}, in {func_name}(): {exc}"
        )
        logger.debug(f"Full traceback:\n{tb_str}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "details": {
                    "message": "An error occurred, please try again.",
                    "error": str(exc),
                    "location": f"{file_name}:{line_number} in {func_name}()",
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
    """
    Main entry point for the FastAPI application.
    """
    # from app.utils.config.logging import setup_logging

    # Export env for use inside create_app()
    os.environ["ENV"] = env
    if json_config_path:
        os.environ["JSON_CONFIG_PATH"] = json_config_path

    # # Setup logging before Uvicorn starts
    # setup_logging()

    # Validation note: reload mode doesn't support workers > 1
    if reload and workers > 1:
        click.echo(
            "⚠️ Reload mode does not support multiple workers. Ignoring --workers."
        )
        workers = 1

    # Load configs
    loader = ConfigLoader()
    configs = loader.get_config()
    app_name = configs.get("app_name", "userverse")
    version = configs.get("version", "1.0.0")


    # Launch using factory to ensure consistent app creation
    click.echo(f"🚀 Starting Userverse API on http://{host}:{port} [env={env}]")
    uvicorn.run(
        "app.main:create_app",
        factory=True,
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_config=None,  # Add this parameter
        use_colors=False,  # Disable colored logs for clean JSON
    )


if __name__ == "__main__":
    main()
