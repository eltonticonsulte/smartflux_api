# -*- coding: utf-8 -*-
import json
from requests import get, Response, post
import logging


class ApiTelegram:
    chat_id = "-1001680431972"
    token_bot = "2133038248:AAF7a-Azb5xm_RDg03_uqs0SpoXHvoP50t8"

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)

    def update_id(self) -> None:
        url_update = f"https://api.telegram.org/bot{self.token_bot}/getUpdates"
        try:
            result: Response = get(url_update, timeout=10)
            # if result["ok"] is False return result["error_code"]
            if result.status_code != 200:
                data_json = json.loads(result.content)
                self.log.error(data_json["description"])
            else:
                data_json = json.loads(result.content)

                self.log.debug(json.dumps(data_json, indent=4, sort_keys=True))

                self.chat_id = data_json["result"][-1]["message"]["chat"]["id"]
                msg_bot = data_json["result"][-1]["message"]["text"]
                self.msg_bot = msg_bot.lower()
        except Exception as error:
            self.log.debug(error)

    def send_msg(self, message: str) -> None:

        url = f"https://api.telegram.org/bot{self.token_bot}/sendMessage?chat_id={self.chat_id}&text={message}"
        try:
            result: Response = post(url, timeout=10)
            if result.status_code != 200:
                data_json = json.loads(result.content)
                self.log.error(data_json["description"])
            else:
                self.log.debug(f"aviso bot {message} ok")
        except Exception as error:
            self.log.error(error)


if __name__ == "__main__":
    print("run")
    ob = ApiTelegram()
    ob.update_id()
    ob.send_msg("teste")
