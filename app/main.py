import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.parcels import router as parcels_router
from app.exceptions.parcels import ParcelNotFoundError
from app.core.logging import setup_logging
from loguru import logger

setup_logging()

app = FastAPI()
app.include_router(parcels_router)



SESSION_COOKIE = "sid"
IGNORED_PATHS = {"/favicon.ico"}

@app.exception_handler(ParcelNotFoundError)
async def parcel_not_found_handler(
    _request: Request,
    _exc: ParcelNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": "Parcel not found"},
    )





import time

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    if request.url.path in IGNORED_PATHS:
        return await call_next(request)

    sid = request.cookies.get(SESSION_COOKIE) or str(uuid.uuid4())
    request.state.session_id = sid

    start = time.perf_counter()
    with logger.contextualize(sid=sid, path=request.url.path, method=request.method):
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("Unhandled error")
            raise
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info("HTTP {method} {path} -> {status} ({ms:.1f}ms)",
                    method=request.method,
                    path=request.url.path,
                    status=response.status_code,
                    ms=elapsed_ms)

    if SESSION_COOKIE not in request.cookies:
        response.set_cookie(
            key=SESSION_COOKIE,
            value=sid,
            httponly=True,
            path="/",
            samesite="lax",
        )
        logger.info("New session created")

    return response


