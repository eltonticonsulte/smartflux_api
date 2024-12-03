# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    token_api = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    zones = relationship("Zone", back_populates="user")


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    users_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="zones")
    devices = relationship("Device", back_populates="zone")


class EventCounter(Base):
    __tablename__ = "eventCounter"

    id = Column(Integer, primary_key=True)
    event_time = Column(DateTime, default=datetime.utcnow)
    channel_id = Column(Integer, nullable=False)
    count_in = Column(Integer, default=0)
    count_out = Column(Integer, default=0)

    # You might want to add a relationship to Device or Channel if applicable


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    id_zona = Column(Integer, ForeignKey("zones.id"), nullable=False)
    metadate = Column(JSON, nullable=True)  # Using JSON for flexible metadata

    # Relationships
    zone = relationship("Zone", back_populates="devices")
