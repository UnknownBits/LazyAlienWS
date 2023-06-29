from lazyalienws.server.core import _websocket_server, _websocket_qq_client
from lazyalienws.api.data import Config
from lazyalienws.server.default.conf import DEFAULT_CONF
import os, time

INTERVAL_TIME = 5

def makedirs(path: list):
    for p in path:
        if os.path.exists(p):
            return True
        else:
            os.makedirs(p)

def start():
    print("server will start in %ssec"%INTERVAL_TIME)
    time.sleep(INTERVAL_TIME)
    if conf_qq["active"]:
        server.QQclient = QQclient
        QQclient.start()
    server.start()

print("PATH : %s"%(os.getcwd()))

makedirs(["plugins","data","conf"])

conf = Config("conf.json",default_data=DEFAULT_CONF,filepath="").load()
conf_server = conf["websocket"]
conf_qq = conf["QQclient"]

server = _websocket_server.LASWebsocketServer(host=conf_server["host"])
if conf_qq["active"]:
    QQclient = _websocket_qq_client.QQWebSocketClient(url=conf_qq["cqhttp"], server=server, qq_groups=conf_qq["groups"], admin=conf_qq["admin"])