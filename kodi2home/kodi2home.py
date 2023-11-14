import asyncio
from pykodi import get_kodi_connection, Kodi, CannotConnectError, InvalidAuthError

# from jsonrpc_websocket import Server
import signal
import functools
import websockets
import json
import sys

import logging

logging.basicConfig(
    format="%(asctime)s %(message)s", level=logging.INFO, stream=sys.stdout
)
# put this in gen.xml
# <volume_up>NotifyAll("kodi2home", "kodi_call_home", {"trigger":"automation.volume_up"})</volume_up>

loop = asyncio.get_event_loop()


def ask_exit(signame):
    print("got signal %s: exit" % signame)
    loop.stop()


class kodi2home:
    id_nr = 1

    def __init__(self, config_file):
        with open(config_file, "r") as inputfile:
            self.config = json.load(inputfile)
        pass

    async def connect_to_kodi(self):
        logging.info(
            f"kodi settings: {self.config['kodi_adress']},  {self.config['kodi_http_port']} {self.config['kodi_ws_port']}, {self.config['kodi_username']}, , {self.config['kodi_password']}"
        )
        self.kodi_connection = get_kodi_connection(
            self.config["kodi_adress"],
            self.config["kodi_http_port"],
            self.config["kodi_ws_port"],
            self.config["kodi_username"],
            self.config["kodi_password"],
            False,
            5,
            None,
        )
        await self.kodi_connection.connect()
        self.kodi = Kodi(self.kodi_connection)

        self.kodi_connection.server.Other.kodi_call_home = self.kodi_call_home

        properties = await self.kodi.get_application_properties(["name", "version"])
        logging.info(f"Kodi is connected {properties}")
        await self.kodi.ping()
        await self.kodi_connection.server.Input.ExecuteAction("reloadkeymaps")

    async def connect_to_home(self):
        logging.info(
            f"Home assistant settings: {self.config['home_adress']},  {self.config['home_ssl']}, {sys.argv[1]}"
        )
        if self.config["home_ssl"]:
            home_ssl = True
        else:
            home_ssl = None
        self.websocket = await websockets.connect(
            self.config["home_adress"], ssl=home_ssl
        )
        login_org = {"type": "auth", "access_token": sys.argv[1]}
        data = await self.websocket.recv()
        logging.info(f"Home Assistant: {data}")
        await self.websocket.send(json.dumps(login_org))
        data = await self.websocket.recv()
        logging.info(f"Home Assistant: {data}")

    async def kodi_call_home(self, sender, data):
        if "trigger" not in data:
            return

        self.id_nr += 1
        service_call = {
            "id": self.id_nr,
            "type": "call_service",
            "domain": "automation",
            "service": "trigger",
            "service_data": {
                "entity_id": data["trigger"],
            },
        }

        logging.info(f"{sender} is calling home {json.dumps(service_call)}")
        try:
            await self.websocket.send(json.dumps(service_call))
        except websockets.exceptions.ConnectionClosedOK:
            await self.websocket.close()
            await self.connect_to_home()
            logging.info(f"reconnect on oke connection close")
            await self.websocket.send(json.dumps(service_call))
        except websockets.exceptions.ConnectionClosedError:
            await self.websocket.close()
            await self.connect_to_home()
            logging.info(f"reconnect on way to fast pressing buttons")
            await self.websocket.send(json.dumps(service_call))


    async def run(self):
        try:
            await self.connect_to_kodi()
        except CannotConnectError:
            logging.error("Reconnecting failed, try again")
        except InvalidAuthError:
            logging.error("InvalidAuthError, wrong login")
            return

        await self.connect_to_home()
        logging.info("connected")
        while 1:
            try:
                if self.kodi_connection.connected:
                    await self.kodi.ping()
                else:
                    await self.connect_to_kodi()
            except CannotConnectError:
                logging.error("Reconnecting failed, try again")
            except InvalidAuthError:
                logging.error("InvalidAuthError, wrong login")
                return
            await asyncio.sleep(10)
        logging.info("Done")


def main():
    for signame in ("SIGINT", "SIGTERM"):
        loop.add_signal_handler(
            getattr(signal, signame), functools.partial(ask_exit, signame)
        )

    try:
        k = kodi2home("options.json")
        loop.run_until_complete(k.run())
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    main()

# 	loop.run_until_complete()


# ref:
# 	https://github.com/lijinqiu1/homeassistant/blob/master/websocketAPI.py
# 	https://developers.home-assistant.io/docs/api/websocket#calling-a-service
# 	https://forums.homeseer.com/forum/media-plug-ins/media-discussion/kodi-xbmc-spud/76271-how-to-trigger-hs-events-from-kodi-xbmc-interface
# 	https://www.home-assistant.io/integrations/kodi/
# 	https://github.com/home-assistant/core/blob/dev/homeassistant/components/kodi/media_player.py
# 	https://github.com/OnFreund/PyKodi/blob/master/pykodi/kodi.py
# 	https://github.com/emlove/jsonrpc-websocket
# 	https://kodi.wiki/view/Keymap#Add-on_built-in.27s
# 	https://github.com/xbmc/xbmc/blob/master/system/keymaps/keyboard.xml
# 	https://github.com/home-assistant/core/blob/dev/homeassistant/components/kodi/__init__.py
