from pydantic import BaseModel


class EmailSenderSchoolInput(BaseModel):
    sender_id: str
    cod_school: str
