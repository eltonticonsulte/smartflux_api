# -*- coding: utf-8 -*-
from src.database.connect import DBConnectionHandler
from src.database.schema import Empresa
from core.config import get_settings

print(get_settings().dict())
if __name__ == "__main__":
    with DBConnectionHandler() as eng:
        with eng.transaction():
            Empresa.metadata.create_all(eng.get_engine())
            print("Database created")
