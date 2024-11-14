from config import MODEL_NAME, OPENAPI_KEY

from langchain import OpenAI


llm = OpenAI(api_key=OPENAPI_KEY, model_name=MODEL_NAME, temperature=0.7)
