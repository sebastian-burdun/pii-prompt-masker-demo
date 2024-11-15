import logging
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from llm_client import llm_client
from pii_masker import pii_masker


app = FastAPI()


logger = logging.getLogger("uvicorn.error")


class QuestionData(BaseModel):
    prompt: str
    context: str


class AnswerData(BaseModel):
    response: str


@app.post("/generate-answer", response_model=AnswerData)
def generate_answer(question_data: QuestionData) -> Any:
    unmasked_question = " ".join([question_data.context, question_data.prompt])
    logger.debug(f"Original question: `{unmasked_question}`")
    masked_question = pii_masker.clean(unmasked_question)
    logger.debug(f"Question to LLM: `{masked_question}`")

    return StreamingResponse(
        pii_masker.unmask_tokens(llm_client.stream(masked_question)),
        media_type="text/event-stream",
    )
