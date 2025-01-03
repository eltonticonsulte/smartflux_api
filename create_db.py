# -*- coding: utf-8 -*-
from src.database.connect import DBConnectionHandler
from src.database.schema import Usuario, UserRole
from src.services import UserServices
from src.repository import UserRepository
from src.dto import CreateUserRequest
from core.config import get_settings


def create_user_admin():
    auth_services = UserServices(UserRepository())
    user = CreateUserRequest(username="admin", password="admin123", role=UserRole.ADMIN)
    user3 = CreateUserRequest(
        username="admin3", password="admin123", role=UserRole.ADMIN
    )
    auth_services.create(user3)

    return auth_services.create(user)


if __name__ == "__main__":

    print("Criando tabelas...", get_settings().DATABASE_URL)
    engine = DBConnectionHandler.get_engine(get_settings().DATABASE_URL)
    Usuario.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
    print("Admin criado com sucesso!", create_user_admin())
