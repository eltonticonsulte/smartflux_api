# -*- coding: utf-8 -*-
import websocket
import requests


def login(user, password):
    data = {"username": user, "password": password}
    response = requests.post("http://localhost:8002/api/user/login", data=data)
    return response.json()


def connect_to_websocket():
    uri = f"ws://localhost:8002/api/event/ws"  # Substitua localhost:8002 pelo endereço correto do servidor

    def on_message(ws, message):
        print(f"Mensagem recebida: {message}")

    def on_error(ws, error):
        print(f"Erro: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("Conexão encerrada")

    def on_open(ws):
        print(f"Conectado ao WebSocket")
        ws.send("Olá, servidor!")  # Mensagem inicial para o servidor

    name_filial = "Filial"
    password = "filial123"
    headers = {
        "Authorization": f"Bearer {login(name_filial, password)['access_token']}"
    }
    ws = websocket.WebSocketApp(
        uri, on_message=on_message, on_error=on_error, on_close=on_close, header=headers
    )
    ws.on_open = on_open

    ws.run_forever()


if __name__ == "__main__":
    connect_to_websocket()
