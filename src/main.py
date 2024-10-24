""" Extract data from SQLite load to PostgresSQL """
import os
import sys

import uvicorn
from fastapi import FastAPI

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.v1.etl import router as etl_router
from src.api.v1.postgres import router as pg_router
from src.api.v1.sqlite import router as sqlite_router
from src.core.config import log_settings
from src.middleware import LoggingMiddleware

app = FastAPI(
    debug=False,
    title='Extract data from SQLite - Transform - Load to PostgresSQL',
    version='1.0.0',
    description='Extract data from SQLite - Transform - Load to PostgresSQL',
    openapi_url='/api/openapi.json',
    docs_url='/api/openapi',
    redoc_url='/api/redoc',
)
app.add_middleware(LoggingMiddleware)

app.include_router(etl_router)
app.include_router(sqlite_router)
app.include_router(pg_router)


if __name__ == '__main__':

    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        log_config=log_settings.log_config_filename,
        app_dir='./src',
        reload=True,
    )
