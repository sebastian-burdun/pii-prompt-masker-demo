import os

from dotenv import load_dotenv


load_dotenv()


OPENAPI_KEY = os.getenv('OPENAPI_KEY')
if not OPENAPI_KEY:
    raise RuntimeError("`OPENAPI_KEY` variable needs to be configured in `.env` file")

MODEL_NAME = os.getenv('MODEL_NAME', "text-davinci-003")
