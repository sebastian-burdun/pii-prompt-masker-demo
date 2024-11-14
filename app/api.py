from typing import Any

from fastapi import FastAPI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

from llm_client import llm
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
    # # Define a simple prompt template
    # template = PromptTemplate.from_template("Write a friendly introduction for {name}.")

    # # Create a chain that links the prompt template and the LLM
    # llm_chain = LLMChain(prompt=template, llm=llm)

    # # Define input for the prompt
    # input_data = {"name": "Alice"}

    # # Execute the chain and print the result
    # result = llm_chain.run(input_data)
    # print(result)


    # debug = os.getenv('DEBUG')

    # print("Database URL:", database_url)
    # print("Secret Key:", secret_key)
    # print("Debug Mode:", debug)
    original_answer = masked_question
    unmasked_answer = pii_masker.unmask(original_answer)
    return {
        "response": unmasked_answer,
    }
