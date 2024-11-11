from fastapi import FastAPI
import nltk
import scrubadub, scrubadub_stanford

nltk.download('punkt_tab')

app = FastAPI()
scrubber = scrubadub.Scrubber()
scrubber.add_detector(scrubadub_stanford.detectors.StanfordEntityDetector)

@app.get("/")
def read_root():
    # obfuscation_mapping = {}

    # def create_obfuscation_mapping(dirty_text, clean_text, **kwargs):
    #     mapping[dirty_text] = clean_text

    # text = (
    #     "John's phone number is 555-123-4567. He lives at 123 Maple Street "
    #     "in San Francisco, and his email is john.doe@example.com."
    # )
    # scrubbed_text = scrubber.clean(
    #     text,
    #     callback=create_obfuscation_mapping,
    # )
    scrubber.clean("My name is John and I work at the United Nations in Geneva")
    import ipdb; ipdb.set_trace()
    return {"Hello": "World"}
