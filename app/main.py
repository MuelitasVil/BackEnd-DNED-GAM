from fastapi import FastAPI
from app.controllers import test_controller
from app.controllers import csv_gam_files_controllers
from app.controllers import gam_user_controller
from app.controllers import gam_group_controller

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World GAM"}


app.include_router(test_controller.router)
app.include_router(csv_gam_files_controllers.router)
app.include_router(gam_user_controller.router)
app.include_router(gam_group_controller.router)
