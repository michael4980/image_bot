import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int


@dataclass
class Rd:
    host: str
    port: int
    db: int
    
    
@dataclass
class tg_bot:
    token: str
    admin_id: int
    api_url: str
    rand: str

@dataclass
class Config:
    res: Rd
    db: DbConfig
    tg_bot: tg_bot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    return Config(
        res = Rd(**config["rs"]),
        db = DbConfig(**config["db"]),
        tg_bot = tg_bot(**config["tg_bot"])
    )