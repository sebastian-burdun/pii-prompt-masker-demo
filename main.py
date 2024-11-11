from fastapi import FastAPI
import scrubadub

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
