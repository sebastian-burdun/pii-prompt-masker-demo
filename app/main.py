from fastapi import FastAPI
import nltk
import scrubadub, scrubadub_address, scrubadub_stanford

nltk.download("punkt_tab")

app = FastAPI()
obfuscator = scrubadub.Scrubber()
obfuscator.add_detector(scrubadub_stanford.detectors.StanfordEntityDetector)
obfuscator.add_detector(scrubadub_address.detectors.AddressDetector)

TEST_TEXT = """
John's phone number is 555-123-4567. He lives at 123 Maple Street
in San Francisco, and his email is john.doe@example.com.
"""


@app.get("/")
def read_root():
    obfuscation_mapping = {}

    def create_obfuscation_mapping(original_text, obfuscated_text, **kwargs):
        obfuscation_mapping[original_text] = obfuscated_text

    obfuscated_text = obfuscator.clean(
        TEST_TEXT,
        callback=create_obfuscation_mapping,
    )
    return {
        "input_text": TEST_TEXT,
        "output_text": obfuscated_text,
        "mapping": obfuscation_mapping,
    }
