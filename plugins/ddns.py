import requests, datetime, http, threading, time
from tcping import Ping
from lazyalienws.api.data import Config

class DDNS:

    def __init__(self, server) -> None:
        self.server = server
        self.latest_checktime = datetime.datetime.now()
        self.latest_checkinfo = None
        self.config = Config("ddns.json", default_data={
            "domain_name":"",
            "port":25565,
            "payload":"",
            "headers":{
               'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
               'Accept': '*/*',
               'Host': 'dnsapi.cn',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded'
            },
            "api":"dnsapi.cn",
            "request":"/Record.Modify",
            "admin":2196226582
        }).load()
    
    def get_address(self):
        server = self.server
        try:
            res = requests.get('http://myip.ipip.net', timeout=5).text
            for i in res.split(' '):
                if 'IP' in i:
                    res = i
                    break
            res = res.replace('IP：','')
            server.logger.info(f'Successfully get ipv4 address : {res}', module_name="DDNS/get-address")
            return res
        except Exception as e:
            server.logger.warn('Failed to get ipv4 address!', warn=e, module_name="DDNS/get-address")
    
    def send_address(self, ipv4_address):
        server = self.server
        config = self.config
        try:
            res = ipv4_address
            conn = http.client.HTTPSConnection(config["api"])
            payload = config["payload"].replace(r"{res}",res)
            headers = config["headers"]
            conn.request("POST", config["request"], payload, headers, )
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8").replace('"weight":null','')
            server.logger.info(f'DATA / {data}, {type(data)}', module_name="DDNS/send-address")
            server.logger.info("payload: %s"%payload)
            server.logger.info(f'Successfully send ipv4 address', module_name="DDNS/send-address")
            try:
                data = dict(eval(data))['status']['message']
                server.logger.info(data, module_name="DDNS/send-address")
                # return data
                return data
            except Exception as e:
                server.logger.warn("Failed to process data: ",warn=e, module_name="DDNS/send-address")
                return "Unknown"
        except Exception as e:
            server.logger.warn(f'Failed to send ipv4 address',warn=e, module_name="DDNS/send-address")
        
    def get_status(self):
        'if well-connected -> connection status; else -> False'
        config = self.config
        try:
            p = Ping(config["domain_name"], config["port"])
            print(self.server.logger.log("",level="INFO", module_name="DDNS/get-status"),end='')
            p.ping(1)
            print(end='> ')
            if '100.00% success rate' in p.result.raw:
                return p.result.raw.split("\n")[2]
            else:
                return False
        except:
            return False
    
    def update(self):
        status = self.get_status()
        self.latest_checktime = datetime.datetime.now()
        if status == False:
            info = self.send_address(self.get_address())
            self.server.logger.info("IP address changed. Updated.", module_name="DDNS/update")
            self.latest_checkinfo = "DDNS/update: %s"%info
            return True
        else:
            self.server.logger.info("Well connected.", module_name="DDNS/update")
            self.latest_checkinfo = "Well connected: "+status
            return False
    
    def start(self):
        global update_thread
        t = threading.Thread(target=self.update)
        t.daemon = True
        t.start()
        update_thread = threading.Timer(900, self.start)
        update_thread.daemon = True
        update_thread.start()

def on_start(server):
    global ddns_server
    ddns_server = DDNS(server)
    f = lambda: (server.logger.info("DDNS server will start in 5s...",module_name="DDNS"),time.sleep(5),ddns_server.start())
    t = threading.Thread(target=f)
    t.start()
    

def on_qq_message(QQclient, server, message):

    # #解析: 检查解析状态
    if message["message"] == "#解析":
        interval = (datetime.datetime.now()-ddns_server.latest_checktime).seconds
        if interval <= 330:
            ddns_status = "DDNS正常运行 检查间隔:5min"
        else:
            ddns_status = "DDNS异常 [CQ:at,qq=%s]"%(ddns_server.config["admin"])
        msg = f'''{ddns_status}
{ddns_server.latest_checktime.strftime("%Y-%m-%d %H:%M:%S")} ({interval}s before):
{ddns_server.latest_checkinfo}
解析* 以重新检查解析
解析$ 以强制解析'''.replace("\n\n","\n")
    
    # #解析* 手动检查解析状态
    elif message["message"] == "#解析*":
        ddns_server.update()
        msg = f'''解析*
{ddns_server.latest_checktime.strftime("%Y-%m-%d %H:%M:%S")}
{ddns_server.latest_checkinfo}'''.replace("\n\n","\n")
    
    # #解析$ 强制进行解析
    elif message["message"] == "#解析$":
        if message["sender"]["user_id"] not in QQclient.admin:
            msg = '''解析$ 权限不足'''
        else:
            info = ddns_server.send_address(ddns_server.get_address())
            server.logger.info("Command from QQ. Updated.", module_name="DDNS/update")
            ddns_server.latest_checkinfo = "QQ/%s: %s"%(message["sender"]["user_id"],info)
            ddns_server.latest_checktime = datetime.datetime.now()
            msg = f'''解析$
{ddns_server.latest_checktime.strftime("%Y-%m-%d %H:%M:%S")}
{ddns_server.latest_checkinfo}'''.replace("\n\n","\n")

    else:
        return
    
    QQclient.send_msg(msg, message)
