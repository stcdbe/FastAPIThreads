from pydantic import BaseModel


class TokenGet(BaseModel):
    access_token: str
    token_type: str
