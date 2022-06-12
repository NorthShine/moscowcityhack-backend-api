"""
Build FastAPI application.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from db import database
from schemas import Settings
from views.admin import admin_router
from views.parser import parser_router
from views.trust_badge import trust_badge_router
from views.statistics import statistics_router

app = FastAPI()
app.include_router(admin_router)
app.include_router(parser_router)
app.include_router(trust_badge_router)
app.include_router(statistics_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup():
    """Connect to the database during startup app."""
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    """Disconnect from the database during shutdown app."""
    await database.disconnect()


@AuthJWT.load_config
def get_config():
    """Get config for AutoJWT."""
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    """Exception handler for AutoJWT."""
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
    )
