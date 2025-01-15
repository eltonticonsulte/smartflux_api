# -*- coding: utf-8 -*-
import requests
from uuid import uuid4

user = "admin"
password = "admin123"


def login(user, password):
    data = {"username": user, "password": password}
    response = requests.post("http://localhost:8002/api/user/login", data=data)
    return response.json()


def create_empresa(name: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name}
    response = requests.post(
        "http://localhost:8002/api/empresa/create", headers=headers, json=data
    )
    return response.json()


def create_filial(name: str, empresa_id: int, token: str, cnpj: str):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name_filial": name, "empresa_id": empresa_id, "cnpj": cnpj}
    response = requests.post(
        "http://localhost:8002/api/filial/create", headers=headers, json=data
    )
    return response.json()


def create_zone(name: str, filial_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "filial_id": filial_id}
    response = requests.post(
        "http://localhost:8002/api/zone/create", headers=headers, json=data
    )
    return response.json()


def create_camera(name: str, zone_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "zone_id": zone_id}
    response = requests.post(
        "http://localhost:8002/api/camera/create", headers=headers, json=data
    )
    return response.json()


data_user = login(user, password)
token = data_user["access_token"]
print("criando empresa #####################")
empresa = create_empresa(f"Empresa {uuid4().hex}", token)
print(empresa)
print("criando filial #####################")
id_empresa = empresa["empresa_id"]

filial = create_filial(f"Filial1_{uuid4().hex}", id_empresa, token, "123456789")
print(filial)
filial_id = filial["filial_id"]
print("criando zona #####################")
zona = create_zone(f"Zona1_{uuid4().hex}", filial_id, token)
print(zona)
zona_id = zona["zone_id"]

print("criando camera #####################")
camera = create_camera(f"Camera_{uuid4().hex}", zona_id, token)

print(camera)
