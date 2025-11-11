from pydantic import BaseModel


class EmailSenderHeadquartersInput(BaseModel):
    sender_id: str
    cod_headquarters: str
