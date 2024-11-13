from fastapi import FastAPI
import nltk
from pydantic import BaseModel
import scrubadub, scrubadub_address, scrubadub_stanford

nltk.download("punkt_tab")


class ObfuscationMappingBuilder(scrubadub.post_processors.PostProcessor):
    name = "obfuscation_mapping_builder"
    obfuscation_mapping = {}

    def process_filth(self, filth_list):
        for filth in filth_list:
            self.obfuscation_mapping[filth.replacement_string] = filth.text
        return filth_list


app = FastAPI()
obfuscator = scrubadub.Scrubber(
    post_processor_list=[
        scrubadub.post_processors.FilthReplacer(
            include_hash=True, hash_salt="example", hash_length=5
        ),
        ObfuscationMappingBuilder(),
    ]
)
obfuscator.add_detector(scrubadub_stanford.detectors.StanfordEntityDetector)
obfuscator.add_detector(scrubadub_address.detectors.AddressDetector)


class ObfuscationData(BaseModel):
    prompt: str
    context: str


@app.post("/generate-answer")
def generate_answer(obfuscation_data: ObfuscationData):
    original_text = " ".join([obfuscation_data.prompt, obfuscation_data.context])
    llm_request_text = obfuscator.clean(original_text)
    obfuscation_mapping = next(
        processor
        for processor in obfuscator._post_processors
        if isinstance(processor, ObfuscationMappingBuilder)
    ).obfuscation_mapping

    llm_response_text = llm_request_text
    for obfuscated_item, clarified_item in obfuscation_mapping.items():
        llm_response_text = llm_response_text.replace(obfuscated_item, clarified_item)

    return {
        "original_text": original_text,
        "llm_request_text": llm_request_text,
        "llm_response_text": llm_response_text,
    }
