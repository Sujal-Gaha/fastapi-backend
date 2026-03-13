from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_config
from app.core.exceptions import DuplicateEmailError
from app.core.logging import logger
from app.middleware import RequestIDMiddleware

from app.api.v1 import router as v1_router

config = get_config()

app = FastAPI(
    title=config.server.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{config.server.BASE_API_PATH}/docs.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.WHITELISTED_ORIGINS,
    allow_credentials=True,
)
app.add_middleware(RequestIDMiddleware)


@app.exception_handler(DuplicateEmailError)
async def duplicate_email_handler(req: Request, exc: DuplicateEmailError):
    logger.warning(f"Duplicate email: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": str(exc), "is_success": False},
    )


@app.exception_handler(Exception)
async def generic_expression_handler(req: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": f"Internal server error\n{exc}", "is_success": False},
    )


app.include_router(v1_router, prefix=config.server.BASE_API_PATH)


@app.get("/")
async def hello_from_the_server():
    return "Hello from the FastAPI server"


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Log config summary at startup
config.log_summary(logger)
