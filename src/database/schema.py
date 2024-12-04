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
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

Base = declarative_base()


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    data_criacao = Column(DateTime, default=func.now())

    filiais = relationship("Filial", backref="empresa", cascade="all, delete-orphan")


class Filial(Base):
    __tablename__ = "filiais"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cnpj = Column(String(18), nullable=False)
    password_hash = Column(String, nullable=False)
    token_api = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    # Relationships
    zones = relationship("Zone", backref="filial", cascade="all, delete-orphan")


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    filial_id = Column(Integer, ForeignKey("filiais.id"), nullable=False)

    camera = relationship("Camera", backref="zone", cascade="all, delete-orphan")


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    zona_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    metadate = Column(JSON, nullable=True)  # Using JSON for flexible metadata

    # Relationships

    eventos = relationship(
        "EventCountTemp", backref="camera", cascade="all, delete-orphan"
    )
    event_count_hourly = relationship(
        "EventCountHourly", backref="camera", cascade="all, delete-orphan"
    )


class EventCountTemp(Base):
    __tablename__ = "event_count_temp"
    __table_args__ = (
        Index("idx_camera_timestamp", "camera_id", "event_time"),
        UniqueConstraint("camera_id", "event_time"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_time = Column(DateTime, default=func.now())
    count_in = Column(Integer, default=0)
    count_out = Column(Integer, default=0)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)


class EventCountHourly(Base):
    """
    Tabela histórica com eventos agregados por hora e câmera
    """

    __tablename__ = "event_count_hourly"

    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    hour_timestamp = Column(DateTime, nullable=False)
    total_count_in = Column(Integer, default=0, nullable=False)
    total_count_out = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        # Índice para otimizar consultas por câmera e hora
        Index("idx_camera_hour", "camera_id", "hour_timestamp"),
        # Garante unicidade de registro por câmera e hora
        UniqueConstraint("camera_id", "hour_timestamp", name="uq_camera_hour"),
    )
