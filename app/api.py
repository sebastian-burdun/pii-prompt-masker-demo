from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from pii_masker import pii_masker, PIIMaskMapBuilder


app = FastAPI()


class QuestionData(BaseModel):
    prompt: str
    context: str


class AnswerData(BaseModel):
    response: str


@app.post("/generate-answer", response_model = AnswerData)
def generate_answer(question_data: QuestionData) -> Any:
    original_text = " ".join([question_data.prompt, question_data.context])
    question = pii_masker.clean(original_text)
    pii_mask_map = next(
        processor
        for processor in pii_masker._post_processors
        if isinstance(processor, PIIMaskMapBuilder)
    ).mapping

    answer = question
    for masked_item, unmasked_item in pii_mask_map.items():
        answer = answer.replace(masked_item, unmasked_item)

    return {
        "response": answer,
    }
