from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

@asynccontextmanager
async def db_client_lifespan(app: FastAPI):
    setting = get_settings()

    app.state.mongo_conn =  AsyncIOMotorClient( setting.MONGODB_URL )
    app.state.db_client =  app.state.mongo_conn[setting.MONGODB_DATABASE]

    yield
    app.state.mongo_conn.close()


app = FastAPI(lifespan=db_client_lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)
