import pathlib
from pydantic_settings import BaseSettings


class Base(BaseSettings):

    # API section
    project_name: str

    #  DB Postgres section

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent.parent}/.env"
        env_file_encoding = 'utf-8'


settings = Base()