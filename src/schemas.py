from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    jwt_secret_key: str = 'secret'


class Whitelist(BaseModel):
    id: int
    url: str
