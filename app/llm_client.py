from settings import MODEL_NAME, OPENAPI_KEY

from langchain_openai import ChatOpenAI


llm_client = ChatOpenAI(openai_api_key=OPENAPI_KEY, model_name=MODEL_NAME)
