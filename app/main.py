from fastapi import FastAPI
from app.controllers import test_controller
from app.controllers import csv_gam_files_controllers

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World GAM"}


app.include_router(test_controller.router)
app.include_router(csv_gam_files_controllers.router)
