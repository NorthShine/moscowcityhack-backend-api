from pydantic import BaseModel

from config import get_config


class User(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = get_config()['SECRET_KEY']


class Whitelist(BaseModel):
    id: int
    url: str
