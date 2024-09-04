from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm import LLMProviderFactory
from stores.vectordb import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser

@asynccontextmanager
async def clients_lifespan(app: FastAPI):
    setting = get_settings()

    app.state.mongo_conn =  AsyncIOMotorClient( setting.MONGODB_URL )
    app.state.db_client =  app.state.mongo_conn[setting.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(setting)
    vectordb_provider_factory= VectorDBProviderFactory(setting)
    
    # generation client
    app.state.generation_client = llm_provider_factory.create(provider= setting.GENERATION_BACKEND)
    app.state.generation_client.set_generation_model(model_id= setting.GENERATION_MODEL_ID)

    # embedding client
    app.state.embedding_client = llm_provider_factory.create(provider= setting.EMBEDDING_BACKENT)
    app.state.embedding_client.set_embedding_model(model_id= setting.EMBEDDING_MODEL_ID,
                                                   embedding_size= setting.EMBEDDING_MODEL_SIZE)
    
    # vectordb client
    app.state.vector_db_client = vectordb_provider_factory.create(
        provider= setting.VECTOR_DB_BACKEND
    )
    
    app.state.vector_db_client.connect()

    app.state.template_parser = TemplateParser(
        language=setting.PRIMARY_LANGUAGE,
        default_language=setting.DEFAULT_LANGUAGE,
    )

    yield
    app.state.mongo_conn.close()
    app.state.vector_db_client.disconnect()


app = FastAPI(lifespan=clients_lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)