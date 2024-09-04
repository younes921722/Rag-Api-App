from fastapi import APIRouter, status, Request
from routes.schemes.nlp import PushRequest, SearchRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers.NLPController import NLPController
import logging
from models import ResponseSignal

logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1","nlp"]
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id:str, push_request:PushRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client = request.app.state.db_client
    )

    chunk_model = await ChunkModel.create_instance(
        db_client = request.app.state.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    if not project:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value
            }
        )
    
    nlp_controller = NLPController(
        vector_db_client= request.app.state.vector_db_client,
        generation_client= request.app.state.generation_client,
        embedding_client= request.app.state.embedding_client,
    )

    has_records = True
    page_no = 1
    inserted_items_count = 0
    idx = 0

    while has_records:
        print("0:"*40,inserted_items_count)
        page_chunks = await chunk_model.get_project_chunks(project_id= project.id, page_no= page_no)

        if len(page_chunks):
            page_no +=1

        if not page_chunks or len(page_chunks) == 0 :
            has_records = False
            break

        chunk_ids = list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)

        is_inserted = nlp_controller.index_into_vector_db(
            project= project,
            chunks= page_chunks,
            do_reset= push_request.do_reset,
            chunks_ids=chunk_ids
        )

        if not is_inserted:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.INSERT_INTO_VECTORDB_ERROR.value
            }
        )

        inserted_items_count += len(page_chunks)


        


    return JSONResponse(
            content={
                "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
                "iserted_items_count":inserted_items_count
            }
        )


@nlp_router.get("/index/info/{project_id}")
async def get_project_info(request: Request, project_id:str):

    print("9"*10)
    project_model = await ProjectModel.create_instance(
        db_client = request.app.state.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vector_db_client= request.app.state.vector_db_client,
        generation_client= request.app.state.generation_client,
        embedding_client= request.app.state.embedding_client      
    )

    collection_info = nlp_controller.get_vector_db_collection_info(project=project)

    return JSONResponse(
            content={
                "signal": ResponseSignal.VECTORDB_COLLECTION_RETRIEVED.value,
                "collection_info":collection_info
            }
        )


@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id:str, search_request:SearchRequest):

    project_model = await ProjectModel.create_instance(
        db_client = request.app.state.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vector_db_client= request.app.state.vector_db_client,
        generation_client= request.app.state.generation_client,
        embedding_client= request.app.state.embedding_client,
        template_parser = request.app.state.template_parser      
    )

    responses = nlp_controller.search_index(project=project, query_text=search_request.text, limit= search_request.limit)

    if not responses:

        return JSONResponse(
            content={
                "search signal": ResponseSignal.VECTORDB_SEARCH_ERROR.value,

            }
        )
    
    return JSONResponse(
            content={
                "search signal": ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
                "responses":[response.model_dump() for response in responses]
            }
        )

@nlp_router.post("/index/answer/{project_id}")
async def answer_rag(request: Request, project_id:str, search_request:SearchRequest):

    project_model = await ProjectModel.create_instance(
        db_client = request.app.state.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vector_db_client= request.app.state.vector_db_client,
        generation_client= request.app.state.generation_client,
        embedding_client= request.app.state.embedding_client,
        template_parser = request.app.state.template_parser      
    )

    answer, full_prompt , chat_history = nlp_controller.answer_rag_question(
        project= project,
        query_text= search_request.text,
        limit= search_request.limit,
    )

    if not answer:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.RAG_ANSWER_ERROR.value
            }
        )
    
    return JSONResponse(  
            content={
                "signal": ResponseSignal.RAG_ANSWER_SUCCESS.value,
                "answer":answer,
                "full_prompt":full_prompt,
                "chat_history":chat_history,
            }
        )