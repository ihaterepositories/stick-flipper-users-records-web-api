from app.routes.user_record_route import item_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(item_router)