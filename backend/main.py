import logging
import time

from fastapi import FastAPI, Request

from .app.api import router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spirit-island-api")


app = FastAPI(
    title="Spirit Island Backend",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time.perf_counter()

    logger.info(
        "REQUEST: %s %s",
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start

        logger.info(
            "RESPONSE: %s %s -> %s (%.3fs)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = time.perf_counter() - start

        logger.exception(
            "ERROR: %s %s after %.3fs",
            request.method,
            request.url.path,
            duration,
        )

        raise


app.include_router(router)


@app.get("/")
def root():

    return {
        "name": "Spirit Island Backend",
        "status": "ok",
    }