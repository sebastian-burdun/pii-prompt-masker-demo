from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from pii_masker import pii_masker


app = FastAPI()


class QuestionData(BaseModel):
    prompt: str
    context: str


class AnswerData(BaseModel):
    response: str


@app.post("/generate-answer", response_model = AnswerData)
def generate_answer(question_data: QuestionData) -> Any:
    original_question = " ".join([question_data.prompt, question_data.context])
    masked_question = pii_masker.clean(original_question)
    # LLM call
    original_answer = masked_question
    unmasked_answer = pii_masker.unmask(original_answer)
    return {
        "response": unmasked_answer,
    }
