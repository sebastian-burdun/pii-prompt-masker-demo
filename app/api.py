import logging
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from llm_client import llm_client
from pii_masker import pii_masker


app = FastAPI()


logger = logging.getLogger('uvicorn.error')

class QuestionData(BaseModel):
    prompt: str
    context: str


class AnswerData(BaseModel):
    response: str


@app.post("/generate-answer", response_model=AnswerData)
def generate_answer(question_data: QuestionData) -> Any:
    masked_question = pii_masker.clean(
        " ".join([question_data.context, question_data.prompt])
    )
    logger.debug(f"Question sent to LLM: '{masked_question}'")

    masked_answer = llm_client.predict(masked_question)
    logger.debug(f"Answer received from LLM: '{masked_answer}'")

    return {"response": pii_masker.unmask_answer(masked_answer)}
