# -*- coding: utf-8 -*-
import random
import time
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import hashlib
import uuid
from sqlalchemy.sql import func
from src.database import Empresa, Filial, Zone, Camera, EventCountTemp, EventCount
from src.repository import (
    EmpresaRepository,
    FilialRepository,
    ZoneRepository,
    CameraRepository,
    CountEventRepository,
)

# Configuração da conexão com o banco de dados
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/smartflux"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def gerar_hash():
    """Gera um hash aleatório para senha"""
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()


def gerar_token():
    """Gera um token aleatório"""
    return str(uuid.uuid4())


def clear_table_empresa():
    rpo = EmpresaRepository()
    empresas = rpo.get_all()
    for empresa in empresas:
        rpo.delete(empresa.empresa_id)


def clear_table_filial():
    repo = FilialRepository()
    filiais = repo.get_all()
    for filial in filiais:
        repo.delete(filial.filial_id)


def clear_table_zone():
    repo = ZoneRepository()
    zones = repo.get_all()
    for zone in zones:
        repo.delete(zone.zone_id)


def clear_table_camera():
    repo = CameraRepository()
    cameras = repo.get_all()
    for camera in cameras:
        repo.delete(camera.channel_id)


def create_empresa(total: int = 100):
    repo = EmpresaRepository()
    list_id_empresa = []
    for i in range(total):
        empresa = Empresa(
            name=f"Empresas{i}", description=f"Empresa de exemplo para teste {i+1}"
        )
        id_empres = repo.create(empresa)
        list_id_empresa.append(id_empres)
        print("id_empresa:", id_empres)
    return list_id_empresa


def create_filial(id_empresa, total: int = 100):
    repo = FilialRepository()
    list_id_filial = []
    for i in range(total):
        filial = Filial(
            name=f"Filials {i} de {id_empresa}",
            cnpj=f"{random.randint(10000000000000, 99999999999999):014d}",
            description=f"Filial de teste {i+1}",
            empresa_id=id_empresa,
        )
        id_filial = repo.create(filial)
        list_id_filial.append(id_filial)
        print("id filial:", id_filial)
    return list_id_filial


def create_zone(id_filial, total: int = 100):
    repo = ZoneRepository()
    list_id_zone = []
    for i in range(total):
        zone = Zone(name=f"Zonas {i} de {id_filial}", filial_id=id_filial)
        id_zone = repo.create(zone)
        list_id_zone.append(id_zone)
        print("id zone:", id_zone)
    return list_id_zone


def create_camera(id_zone, total: int = 100):
    repo = CameraRepository()
    list_id_camera = []
    for i in range(total):
        camera = Camera(
            name=f"Cameras {i} de {id_zone}",
            zona_id=id_zone,
        )
        id_camera = repo.create(camera)
        list_id_camera.append(id_camera)
        print("id camera:", id_camera)
    return list_id_camera


def popular_banco():
    id_empresa = create_empresa(3)
    for id_emp in id_empresa:
        id_filial = create_filial(id_emp, 4)
        for id_fil in id_filial:
            id_zonas = create_zone(id_fil, 4)
            for id_zone in id_zonas:
                create_camera(id_zone, 10)


def pouplar_evento_day(total: int = 100):
    data = CameraRepository()
    otimize = CountEventRepository()
    all_camer = data.get_all()
    list_data = []
    for camera in all_camer:
        for i in range(total):
            event_count_temp = EventCountTemp(
                channel_id=camera.channel_id,
                event_time=datetime.now() + timedelta(minutes=i),
                count_out=1,
                count_in=1,
            )
            list_data.append(event_count_temp)
            # data.add(event_count_temp)

    otimize.create_all(list_data)
    print("total", len(list_data))


def clear_all():
    clear_table_camera()
    clear_table_zone()
    clear_table_filial()
    clear_table_empresa()


if __name__ == "__main__":
    clear_all()
    popular_banco()
    start = time.time()
    pouplar_evento_day(100)
    end = time.time()
    print("timer", end - start)
