from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool


class UserLoginSchema(BaseModel):
    username: str
    password: str


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenSchema(BaseModel):
    refresh_token: str
