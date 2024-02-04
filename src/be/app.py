from fastapi import FastAPI, HTTPException

from src.be.api.exceptions import http_exception_handler
from src.be.api.routers import router


def make_app() -> FastAPI:
    _app = FastAPI()
    _app.include_router(router)
    _app.add_exception_handler(exc_class_or_status_code=HTTPException, handler=http_exception_handler)
    return _app


app = make_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app)
