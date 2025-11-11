from fastapi import FastAPI
from app.controllers import testClient

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World GAM"}


app.include_router(testClient.router)
