# -*- coding: utf-8 -*-
import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Date,
    JSON,
    ForeignKey,
    Index,
)

from sqlalchemy import Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID as PGUUID

from ..enums import UserRule, CameraState

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRule, name="user_role"), default=UserRule.FILIAL)

    data_criacao = Column(DateTime, default=func.now())
    ultima_modificacao = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Usuario(user_id={self.user_id}, username={self.username}, is_active={self.is_active}, role={self.role}, data_criacao={self.data_criacao}, ultima_modificacao={self.ultima_modificacao})"


class PermissaoAcesso(Base):
    __tablename__ = "permissoes_acesso"

    permissao_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("usuarios.user_id"), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.empresa_id"), nullable=True)
    filial_id = Column(Integer, ForeignKey("filiais.filial_id"), nullable=True)

    user = relationship("Usuario", backref="permissoes")
    empresa = relationship("Empresa", backref="permissoes")
    filial = relationship("Filial", backref="permissoes")

    def __repr__(self):
        return (
            f"PermissaoAcesso(permissao_id={self.permissao_id}, user_id={self.user_id}, empresa_id={self.empresa_id}, "
            f"filial_id={self.filial_id})"
        )


class Empresa(Base):
    __tablename__ = "empresas"

    empresa_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True, default="")
    data_criacao = Column(DateTime, default=func.now())

    filiais = relationship("Filial", back_populates="empresa")

    def __repr__(self):
        return f"Empresa(empresa_id={self.empresa_id}, name={self.name}, token_api={self.token_api}, is_active={self.is_active}, description={self.description}, data_criacao={self.data_criacao})"


class Filial(Base):
    __tablename__ = "filiais"
    filial_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    cnpj = Column(String, nullable=False)
    token_api = Column(
        PGUUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.empresa_id"), nullable=False)
    empresa = relationship("Empresa", back_populates="filiais")
    zones = relationship("Zone", back_populates="filial")


class Zone(Base):
    __tablename__ = "zones"

    zone_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    filial_id = Column(Integer, ForeignKey("filiais.filial_id"), nullable=False)
    filial = relationship("Filial", back_populates="zones")
    camera = relationship("Camera", back_populates="zone")


class Camera(Base):
    __tablename__ = "cameras"
    channel_id = Column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, doc="UUID da camera"
    )
    name = Column(String, nullable=False)
    metadate = Column(JSON, nullable=True)
    worker_id = Column(String, nullable=True)
    zona_id = Column(Integer, ForeignKey("zones.zone_id"), nullable=False)
    status = Column(Enum(CameraState, name="camera_state"), default=CameraState.STOP)
    zone = relationship("Zone", back_populates="camera")
    eventos = relationship("EventCountTemp", backref="camera")
    event_count_hourly = relationship("EventCount", backref="camera")


class EventCountTemp(Base):
    __tablename__ = "event_count_temp"
    __table_args__ = (
        Index("idx_camera_timestamp", "channel_id", "event_time"),
        UniqueConstraint("channel_id", "event_time"),
    )

    count_event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_time = Column(DateTime, default=func.now())
    count_in = Column(Integer, default=0)
    count_out = Column(Integer, default=0)
    channel_id = Column(PGUUID, ForeignKey("cameras.channel_id"), nullable=False)


class EventCount(Base):
    """
    Tabela histórica com eventos agregados por hora e câmera
    """

    __tablename__ = "event_count"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(PGUUID, ForeignKey("cameras.channel_id"), nullable=False)
    date = Column(Date, nullable=False)
    hour = Column(Integer, nullable=False)
    total_count_in = Column(Integer, default=0, nullable=False)
    total_count_out = Column(Integer, default=0, nullable=False)
    filial_id = Column(Integer, ForeignKey("filiais.filial_id"), nullable=False)
    zona_id = Column(Integer, ForeignKey("zones.zone_id"), nullable=False)
    zone_name = Column(String, nullable=False)

    filial = relationship("Filial", backref="event_count")
    zone = relationship("Zone", backref="event_count")

    __table_args__ = (Index("idx_camera_date", "channel_id", "date"),)
