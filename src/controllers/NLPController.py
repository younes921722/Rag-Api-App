import json
from .BaseController import BaseController
from models.db_schemes.project import Project
from typing import List
from models.db_schemes.data_chunk import DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum

class NLPController(BaseController):
    def __init__(self, generation_client, embedding_client, vector_db_client):
        super().__init__()

        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.vector_db_client = vector_db_client

    def creat_collection_name(self, project_id:str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self, project:Project):
        collection_name = self.creat_collection_name(project_id= project.project_id)
        return self.vector_db_client.delete_collection(collection_name= collection_name)

    def get_vector_db_collection_info(self, project:Project):
        collection_name = self.creat_collection_name(project_id= project.project_id)
        collection_info = self.vector_db_client.get_collection_info(collection_name= collection_name)
        print(collection_info)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self, project:Project, chunks: List[DataChunk],
                             chunks_ids : List[int],
                             do_reset:bool = False):
        
        # get collection name
        collection_name = self.creat_collection_name(project_id= project.project_id)

        # manage items
        texts = [ c.chunk_text for c in chunks ]
        metadata = [ c.chunk_metadata for c in chunks ]

        vectors = [

            self.embedding_client.embed_text(text= text,
                                             document_type= DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        # create collection if not exist
        _= self.vector_db_client.create_collection(
            collection_name=collection_name,
                          embedding_size= self.embedding_client.embedding_size,
                          do_reset= do_reset
        )

        # insert into vector db
        _= self.vector_db_client.insert_many(
            collection_name= collection_name, texts=texts, vectors=vectors,
                    metadata= metadata,
                    record_ids = chunks_ids
        )

        return True
    
    def search_index(self, project:Project, query_text:str,
                    document_type:str = DocumentTypeEnum.QUERY.value,
                    limit:int=10):
        
        # get collection name
        collection_name = self.creat_collection_name(project_id= project.project_id)

        # embed the query text
        embedded_query = self.embedding_client.embed_text(query_text,document_type)
        
        if not embedded_query or len(embedded_query) == 0:
            return False
        
        # similarity search by collection name and the query vector
        response = self.vector_db_client.search_by_vector(collection_name,embedded_query,limit)

        if not response:
            return False
        
        
        return json.loads(
            json.dumps(response, default=lambda x: x.__dict__)
        )
