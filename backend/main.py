from fastapi import FastAPI

from .app.api import router


app = FastAPI(
    title="Spirit Island Backend",
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "name": "Spirit Island Backend",
        "status": "ok",
    }