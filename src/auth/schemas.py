from pydantic import BaseModel

class CreateUserModel(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str