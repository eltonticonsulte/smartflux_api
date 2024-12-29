# -*- coding: utf-8 -*-
from src.database.connect import DBConnectionHandler
from src.database.schema import Usuario, UserRole
from src.services import UserServices
from src.repository import UserRepository
from src.dto import CreateUserRequest
from src.mappers import UserMapper
from core.config import get_settings


def create_user_admin():
    auth_services = UserServices(UserRepository())
    user = CreateUserRequest(username="admin", password="admin123", role=UserRole.ADMIN)

    return auth_services.create(user)


if __name__ == "__main__":
    engine = DBConnectionHandler.get_engine(get_settings().DATABASE_URL)
    Usuario.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
    print("Admin criado com sucesso!", create_user_admin())
