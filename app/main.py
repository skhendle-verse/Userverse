from app.utils.app_error import AppError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.configs import configs

# NOTE: Do not call any router that uses the accounting API in this file
from app.routers.user import user

origins = configs.get("cor_origins", ["*"])
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


app.include_router(user.router)


@app.get("/")
async def root():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Welcome to the Userverse backend API",
        },
        #     content={
        #         "status": "ok",
        #         "version": configs.get('version'),
        #         "name": configs.get('name'),
        #         "description": configs.get('description'),
        #         "repository": configs.get('repository'),
        #         "documentation": configs.get('documentation'),
        #         "message": "Welcome to the Userverse backend API",
        # }
    )


# uv run uvicorn app.main:app --port 8500 --reload
