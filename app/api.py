from typing import Any

from fastapi import FastAPI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

from llm_client import llm_client
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
    masked_answer = llm_client.predict(masked_question)
    unmasked_answer = pii_masker.unmask(masked_answer)
    # llm = OpenAI(api_key=api_key, model_name="text-davinci-003", temperature=0.7)
    # template = PromptTemplate.from_template("Write a friendly introduction for {name}.")
    # llm_chain = LLMChain(prompt=template, llm=llm)
    # input_data = {"name": "Alice"}
    # result = llm_chain.run(input_data)

    return {
        "response": unmasked_answer,
    }
