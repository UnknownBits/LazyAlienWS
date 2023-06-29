import threading, time

INTERVAL_TIME = 0.02

def raise_exception(exception:Exception):
    "在不阻塞主程序的情况下抛出异常"
    def func():
        raise exception
    t = threading.Thread(target=func)
    t.start()
    time.sleep(INTERVAL_TIME)