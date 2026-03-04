from fastapi import FastAPI

from app.api.projects import router as projects_router
from app.api.users import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(projects_router)


