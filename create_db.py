# -*- coding: utf-8 -*-
from src.database.connect import DBConnectionHandler
from src.database.schema import Usuario, UserRole
from src.services import UserServices
from src.dto import userDTO
from src.mappers import UserMapper
from core.config import get_settings


def create_user_admin():
    auth_services = UserServices()
    user = userDTO(
        username="admin3",
        password="admin123",
        role=UserRole.ADMIN,
        is_active=True,
    )

    auth_services.create_user(UserMapper.to_entity(user))


if __name__ == "__main__":
    engine = DBConnectionHandler.get_engine(get_settings().DATABASE_URL)
    Usuario.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
    create_user_admin()
