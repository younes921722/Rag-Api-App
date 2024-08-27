from enum import Enum

class LLMEnums(Enum):
    
    OPENAI = "OPENAI"
    GEMINI = "GEMINI"
    COHERE = "COHERE"
    GROQ = "GROQ"
    OLLAMA = "OLLAMA"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CohereEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "CHATBOT"

    DOCUMENT="search_document"
    QUERY="search_query"

class GeminiEnums(Enum):
    DOCUMENT="retrieval_document"
    QUERY="retrieval_query"

class DocumentTypeEnum(Enum):

    DOCUMENT="document"
    QUERY="query"