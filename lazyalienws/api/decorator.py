import threading

def new_thread(func):
    def inner(*args):
        t = threading.Thread(target=func, args=(args))
        t.deamon = True
        t.start()
    return inner