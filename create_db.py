# -*- coding: utf-8 -*-
from src.database.connect import DBConnectionHandler
from src.database.schema import Usuario, UserRole
from core.config import get_settings


def create_user_admin():
    with DBConnectionHandler() as db:
        usuario = Usuario(
            username="admin",
            email="admin@admin.com",
            password_hash="admin123",
            role=UserRole.ADMIN,
        )
        db.add(usuario)
        db.commit()


if __name__ == "__main__":
    engine = DBConnectionHandler.get_engine(get_settings().DATABASE_URL)
    # Usuario.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
    create_user_admin()
