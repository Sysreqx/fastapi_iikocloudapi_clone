from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app import models
from app.database import engine

from app.routers import auth, todos, users

description = """

API v0 documentation.

**Description of common data formats:**

**uuid** - string in UUID(universally unique identifier).
Examples: 550e8400-e29b-41d4-a716-446655440000, b090de0b-8550-6e17-70b2-bbba152bcbd3

**date-time** - date and time string in custom string format **yyyy-MM-dd HH:mm:ss.fff**.
Examples: 2017-04-29 20:45:00.000, 2018-01-01 01:01:30.123


"""

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="iikoCloud API",
        description=description,
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://api-ru.iiko.services/docs/logo"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
