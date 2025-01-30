# -*- coding: utf-8 -*-
import websocket
import requests
import json

server = "btm4q4irvg.us-east-1.awsapprunner.com"
# server = "localhost:8002"


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
            "token": "0c66a137-ff7d-44c4-9813-b7f720fdbb87",
            "message": "Hello, WebSocket!",
        }
        ws.send(json.dumps(payload))

    # password = "filial123"
    # user = login(name_filial, password)
    # print(user)

    headers = {
        "action": "sendMessage",
        "Authorization": f"Bearer ",
    }
    ws = websocket.WebSocketApp(
        uri, on_message=on_message, on_error=on_error, on_close=on_close, header=headers
    )
    ws.on_open = on_open

    ws.run_forever()


if __name__ == "__main__":
    connect_to_websocket()
# request.body.action
