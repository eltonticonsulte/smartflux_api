# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Index,
)
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..common import UserRole, CameraState

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole, name="user_role"), default=UserRole.FILIAL)

    data_criacao = Column(DateTime, default=func.now())
    ultima_modificacao = Column(DateTime, default=func.now(), onupdate=func.now())


class Empresa(Base):
    __tablename__ = "empresas"

    empresa_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    token_api = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    data_criacao = Column(DateTime, default=func.now())

    filiais = relationship("Filial", back_populates="empresa")


class Filial(Base):
    __tablename__ = "filiais"
    filial_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    cnpj = Column(String, nullable=False)
    password_hash = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    token_api = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
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
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, doc="UUID da camera"
    )
    name = Column(String, nullable=False)
    metadate = Column(JSON, nullable=True)
    worker_id = Column(String, nullable=True)
    zona_id = Column(Integer, ForeignKey("zones.zone_id"), nullable=False)
    status = Column(Enum(CameraState, name="camera_state"), default=CameraState.STOP)
    zone = relationship("Zone", back_populates="camera")
    eventos = relationship(
        "EventCountTemp", backref="camera", cascade="all, delete-orphan"
    )
    event_count_hourly = relationship("EventCountHourly", backref="camera")


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
    channel_id = Column(UUID, ForeignKey("cameras.channel_id"), nullable=False)


class EventCountHourly(Base):
    """
    Tabela histórica com eventos agregados por hora e câmera
    """

    __tablename__ = "event_count_hourly"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(UUID, ForeignKey("cameras.channel_id"), nullable=False)
    hour_timestamp = Column(DateTime, nullable=False)
    total_count_in = Column(Integer, default=0, nullable=False)
    total_count_out = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        Index("idx_camera_hour", "channel_id", "hour_timestamp"),
        UniqueConstraint("channel_id", "hour_timestamp", name="uq_camera_hour"),
    )
