import os

from dotenv import load_dotenv


load_dotenv()


OPENAPI_KEY = os.getenv('OPENAPI_KEY')
if not OPENAPI_KEY:
    raise RuntimeError("`OPENAPI_KEY` variable needs to be configured in `.env` file")

DEFAULT_MODEL = "gpt-4o-mini"
MODEL_NAME = os.getenv('MODEL_NAME', DEFAULT_MODEL)
if not MODEL_NAME:
    MODEL_NAME = DEFAULT_MODEL  # case adding `MODEL_NAME=` in `.env`

TOKEN_MASK_PREFIX = "{{"
TOKEN_MASK_SUFFIX = "}}"
