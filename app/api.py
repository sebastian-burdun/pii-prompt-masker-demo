import logging
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from pii_prompt_masker import pii_prompt_masker
from settings import MODEL_NAME, OPENAPI_KEY


app = FastAPI()


llm_client = ChatOpenAI(openai_api_key=OPENAPI_KEY, model_name=MODEL_NAME)


logger = logging.getLogger("uvicorn.error")


class QuestionData(BaseModel):
    prompt: str = Field(example="What is John's phone number?")
    context: str = Field(
        example="John's phone number is 555-123-4567."
        " He lives at 123 Maple Street in San Francisco,"
        " and his email is john.doe@example.com."
    )


class AnswerData(BaseModel):
    response: str = Field(example="John's phone number is 555-123-4567")


@app.post("/generate-answer", response_model=AnswerData)
def generate_answer(question_data: QuestionData) -> Any:
    unmasked_question = " ".join([question_data.context, question_data.prompt])
    logger.debug(f"Original received question: `{unmasked_question}`")
    masked_question = pii_prompt_masker.clean(unmasked_question)
    logger.debug(f"Question sent to LLM: `{masked_question}`")

    return StreamingResponse(
        pii_prompt_masker.unmask_tokens(llm_client.stream(masked_question)),
        media_type="text/event-stream",
    )
