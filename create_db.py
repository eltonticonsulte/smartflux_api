# -*- coding: utf-8 -*-
from src.database.connect import DBConnectionHandler
from src.database.schema import Usuario, UserRule
from src.services import UserServices
from src.repository import UserRepository
from src.dto import RequestCreateUser
from core.config import get_settings


def create_user_admin():
    auth_services = UserServices(UserRepository())
    user = RequestCreateUser(username="admin", password="123", role=UserRule.ADMIN)
    user3 = RequestCreateUser(username="Filial", password="123", role=UserRule.FILIAL)
    auth_services.create(user3)

    return auth_services.create(user)


if __name__ == "__main__":

    print("Criando tabelas...", get_settings().DATABASE_URL)
    engine = DBConnectionHandler.get_engine()
    Usuario.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
    print("Admin criado com sucesso!", create_user_admin())
