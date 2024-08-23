import cohere.client
from ..LLMInterface import LLMInterface
from ..LLMEnums import CohereEnums, DocumentTypeEnum
import cohere
import logging


class CohereProvider(LLMInterface):
    def __init__(self, api_key:str,
                 default_input_max_characters: int=1000,
                 default_generation_output_max_tokens: int=1000,
                 default_generation_temperature: float=0.1):
        
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_output_max_tokens = default_generation_output_max_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None 

        self.client = cohere.Client(api_key=api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id:str, embedding_size:str):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self, text:str):
        return text[:self.default_input_max_characters].strip()
    
    def generate_text(self, prompt: str,chat_history:list=[], max_output_tokens: int=None,
                      temperature: float = None):
        
        if not self.client:
            self.logger.error("Cohere client was not set")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model for Cohere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_output_max_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        response = self.client.chat(
            model = self.generation_model_id,
            chat_history=chat_history,
            message= self.process_text(prompt),
            max_tokens= max_output_tokens,
            temperature= temperature
        )

        if not response or not response.text:
            self.logger.error("Error while generating text with Cohere")
            return None 
        
        chat_history.append(self.constract_prompt(
            role=CohereEnums.ASSISTANT.value,
            prompt=prompt
        ))

        return response.chat_history[-1].message
    

    def embed_text(self, text:str, document_type: str):
        
        if not self.client:
            self.logger.error("Cohere client was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for Cohere was not set")
            return None
    
        input_type = CohereEnums.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CohereEnums.QUERY.value
        
        response = self.client.embed(
            texts= [self.process_text(text)],
            model=self.embedding_model_id,
            input_type= input_type,
            embedding_types=['float']
        )

        if not response or not response.embeddings or not response.embeddings.float_:
            self.logger.error("Error while embedding text with Cohere")
            return None
        
        return response.embeddings.float_[0]
    


    def constract_prompt(self, prompt:str, role:str):
        return {
            "role":role,
            "text": self.process_text(prompt)
        }
    
