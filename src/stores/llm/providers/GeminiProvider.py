import os
import time
import logging
from ..LLMInterface import LLMInterface
from ..LLMEnums import DocumentTypeEnum, GeminiEnums
import google.generativeai as genai

class GeminiProvider(LLMInterface):

    def __init__(self, api_key: str,
                 default_input_max_characters: int = 1000,
                 default_generation_output_max_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_output_max_tokens = default_generation_output_max_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None 

        # Initialize the Generative AI client with the API key
        genai.configure(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                      temperature: float = None):
        pass
    #     if not genai:
    #         self.logger.error("Google Generative AI client was not set")
    #         return None

    #     if not self.generation_model_id:
    #         self.logger.error("Generation model for Google Generative AI was not set")
    #         return None

    #     max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_output_max_tokens
    #     temperature = temperature if temperature else self.default_generation_temperature

    #     # Call to Google Generative AI's text generation API
    #     try:
    #         response = genai.chat(
    #             model=self.generation_model_id,
    #             messages=chat_history + [{"role": "user", "content": self.process_text(prompt)}],
    #             max_output_tokens=max_output_tokens,
    #             temperature=temperature
    #         )
    #     except Exception as e:
    #         self.logger.error(f"Error while generating text with Google Generative AI: {e}")
    #         return None

    #     if not response or not response['candidates']:
    #         self.logger.error("Error while generating text with Google Generative AI")
    #         return None

    #     generated_message = response['candidates'][0]['content']

    #     chat_history.append(self.construct_prompt(
    #         prompt=generated_message,
    #         role=GeminiEnums.ASSISTANT.value
    #     ))

    #     return generated_message

    def embed_text(self, text: str, document_type: str):

        if not genai:
            self.logger.error("Google Generative AI client was not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Google Generative AI was not set")
            return None

        input_type = GeminiEnums.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = GeminiEnums.QUERY.value

        # Call to Google Generative AI's embedding API        
        response = genai.embed_content(
            # model="models/embedding-001",
            model="models/text-embedding-004",
            content= self.process_text(text),
            task_type= input_type,
            
        )

        print("="*40,">>", response['embedding'][:10])
    
        return response['embedding'][:]

    def constract_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
    