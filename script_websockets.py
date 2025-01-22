# -*- coding: utf-8 -*-
import websocket
import requests
import json

# server = "btm4q4irvg.us-east-1.awsapprunner.com"
server = "localhost:8002"


def login(user, password):
    data = {"username": user, "password": password}
    response = requests.post(f"http://{server}/v1/user/login", data=data)
    if response.status_code != 200:
        raise Exception(response.json())
    return response.json()


def connect_to_websocket():
    uri = f"wss://fmqkl4r7pk.execute-api.us-east-1.amazonaws.com/production/"

    def on_message(ws, message):
        print(f"Mensagem recebida: {message}")

    def on_error(ws, error):
        print(f"Erro: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("Conexão encerrada")

    def on_open(ws):
        print(f"Conectado ao WebSocket")
        payload = {
            "action": "sendMessage",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJGaWxpYWwiLCJleHAiOjE3Mzc1Nzk1Njh9.FiiAR7z5XbEM2TkSwh42TniAvSe9_MgkJXdBV1_LhR0",
            "message": "Hello, WebSocket!",
        }
        ws.send(json.dumps(payload))

    name_filial = "Filial"
    # password = "filial123"
    password = "123"
    user = login(name_filial, password)
    print(user)

    headers = {
        "action": "sendMessage",
        "Authorization": f"Bearer {user['access_token']}",
    }
    ws = websocket.WebSocketApp(
        uri, on_message=on_message, on_error=on_error, on_close=on_close, header=headers
    )
    ws.on_open = on_open

    ws.run_forever()


if __name__ == "__main__":
    connect_to_websocket()
# request.body.action
