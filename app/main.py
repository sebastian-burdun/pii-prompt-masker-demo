from fastapi import FastAPI
import nltk
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

TEST_TEXT = """
John's phone number is 555-123-4567. He lives at 123 Maple Street
in San Francisco, and his email is john.doe@example.com.
"""

def initialize_obfuscator():
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

    return obfuscator


@app.get("/")
def read_root():
    obfuscator = initialize_obfuscator()
    obfuscated_text = obfuscator.clean(TEST_TEXT)
    request = TEST_TEXT
    obfuscator = initialize_obfuscator()
    obfuscated_text = obfuscator.clean("Carl")
    obfuscation_mapping = next(
        processor
        for processor in obfuscator._post_processors
        if isinstance(processor, ObfuscationMappingBuilder)
    ).obfuscation_mapping
    response = obfuscated_text
    return {
        "request": request,
        "response": response,
        "mapping": obfuscation_mapping
    }
