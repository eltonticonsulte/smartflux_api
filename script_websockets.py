# -*- coding: utf-8 -*-
import websocket


def connect_to_websocket(filial_id: int):
    uri = f"ws://localhost:8002/api/event/ws"  # Substitua localhost:8002 pelo endereço correto do servidor

    def on_message(ws, message):
        print(f"Mensagem recebida: {message}")

    def on_error(ws, error):
        print(f"Erro: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("Conexão encerrada")

    def on_open(ws):
        print(f"Conectado ao WebSocket da filial {filial_id}")
        ws.send("Olá, servidor!")  # Mensagem inicial para o servidor

    # Configurar o WebSocketApp com callbacks
    ws = websocket.WebSocketApp(
        uri, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open

    # Manter a conexão ativa
    ws.run_forever()


if __name__ == "__main__":
    filial_id = 17  # ID da filial
    connect_to_websocket(filial_id)
