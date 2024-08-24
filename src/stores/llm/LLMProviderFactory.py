from .LLMEnums import LLMEnums
from .providers import OpenAiProvider, CohereProvider
from helpers import Settings

class LLMProviderFactory:
    def __init__(self, config: Settings):
        self.config = config

    def create(self, provider:str):
        
        if provider == LLMEnums.COHERE.value:
            return CohereProvider(
                api_key= self.config.COHERE_API_KEY,
                default_input_max_characters= self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_output_max_tokens= self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature= self.config.GENERATION_DEFAULT_TEMPERATURE,
            )
        
        if provider == LLMEnums.OPENAI.value:
            return OpenAiProvider(
                api_key= self.config.OPENAI_API_KEY,
                api_url= self.config.OPENAI_API_URL,
                default_input_max_characters= self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_output_max_tokens= self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature= self.config.GENERATION_DEFAULT_TEMPERATURE,
            )
        
        return None
    