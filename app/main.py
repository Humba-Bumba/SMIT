from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from api.user_panel import app_insurance
from database.postgres import init_db

from config.settings import settings


app = FastAPI(
    title=f"Read-only API для: {settings.project_name}",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)


# @app.on_event("startup")
# def startup():
#     init_db()


app.include_router(app_insurance.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)