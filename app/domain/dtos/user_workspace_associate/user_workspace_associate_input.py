from pydantic import BaseModel, EmailStr


class UserWorkspaceAssociateInput(BaseModel):
    email_unal: EmailStr
    user_workspace_id: str
    cod_period: str
