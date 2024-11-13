from typing import Any

from fastapi import FastAPI
import nltk
from pydantic import BaseModel
import scrubadub, scrubadub_address, scrubadub_stanford

nltk.download("punkt_tab")


class PIIMaskMapBuilder(scrubadub.post_processors.PostProcessor):
    name = "pii_mask_map_builder"
    mapping = {}

    def process_filth(self, item_list):
        for item in item_list:
            self.mapping[item.replacement_string] = item.text
        return item_list


app = FastAPI()
pii_masker = scrubadub.Scrubber(
    post_processor_list=[
        scrubadub.post_processors.FilthReplacer(
            include_hash=True, hash_salt="example", hash_length=5
        ),
        PIIMaskMapBuilder(),
    ]
)
pii_masker.add_detector(scrubadub_stanford.detectors.StanfordEntityDetector)
pii_masker.add_detector(scrubadub_address.detectors.AddressDetector)


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
