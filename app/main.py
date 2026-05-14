from fastapi import Depends, FastAPI
from app.controllers import test_controller
from app.controllers import csv_gam_files_controllers
from app.controllers import gam_user_controller
from app.controllers import gam_group_controller
from app.controllers import job_controller
from app.utils.auth import get_current_user

app = FastAPI(dependencies=[Depends(get_current_user)])


@app.get("/")
def read_root():
    return {"Hello": "World GAM"}


app.include_router(test_controller.router)
app.include_router(csv_gam_files_controllers.router)
app.include_router(gam_user_controller.router)
app.include_router(gam_group_controller.router)
app.include_router(job_controller.router)
