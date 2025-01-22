# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import time
from random import randint

endpoint = "http://localhost:8002"
# endpoint = "https://btm4q4irvg.us-east-1.awsapprunner.com"


def login(user, password):
    data = {"username": user, "password": password}
    response = requests.post(f"{endpoint}/v1/user/login", data=data)
    if response.status_code != 200:
        raise Exception(response.json())
    return response.json()


def create_event(channel_id: str):
    data = {
        "event_id": 0,
        "channel_id": channel_id,
        "event_time": datetime.now().isoformat() + "Z",
        "count_in": randint(0, 2),
        "count_out": randint(0, 2),
    }
    return data


def sen_data(data: dict, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{endpoint}/v1/event/count", headers=headers, json=data)
    return response


if __name__ == "__main__":
    """
      user_id 4
    "empresa_id": 22,
    "name": "Empresa",
    "is_active": true,
    "data_criacao": "2025-01-15T08:09:17.421803",
    "description": ""


     "filial_id": 17,
    "token": "31f91531-8a6e-42af-ad73-30f311fda2b3",
    "name": "FilialTest",
    "cnpj": "2345456456",
    "is_active": true,
    "empresa_id": 22

      "zone_id": 14,
    "name": "zona01",
    "filial_id": 17

      "zone_id": 15,
      "name": "zona02",
      "filial_id": 17

      "channel_id": "2802d434-1e59-46e3-b9c7-00553000a0ca",
      "name": "camera01",
      "status": 2,
      "zone_id": 14

      "channel_id": "f9b2cbc7-a426-45e2-b987-384196aa8c3f",
      "name": "camera02",
      "status": 2,
      "zone_id": 14
    """
    name_filial = "Filial"
    password = "filial123"
    password = "123"

    print("login   ...")
    user = login(name_filial, password)
    print(user)
    list_chennel = [
        "2802d434-1e59-46e3-b9c7-00553000a0ca",
        "f9b2cbc7-a426-45e2-b987-384196aa8c3f",
    ]
    list_chennel = [
        "5f7fc485-8b5d-4170-82ac-edb1cf3b8ab4",
        "0eb1dcc6-fa4c-4f4e-8e12-b19e03267e94",
    ]
    while True:
        time.sleep(1)
        print("criando evento ...")
        datas = []
        for ch in list_chennel:
            data = create_event(ch)
            datas.append(data)

        response = sen_data(datas, user["access_token"])
        print(response.status_code, response.text)
