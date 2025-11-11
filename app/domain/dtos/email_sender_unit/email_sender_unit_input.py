from pydantic import BaseModel


class EmailSenderUnitInput(BaseModel):
    sender_id: str
    cod_unit: str
