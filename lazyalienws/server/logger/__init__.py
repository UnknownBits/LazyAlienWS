from lazyalienws.server.lib.exception import raise_exception
import datetime

# 日志类
class Logger:

    # 初始化 name日志主模块名
    def __init__(self, name = __name__) -> None:
        self.name = name
        self.loglevel = ["INFO", "WARN"] # 要输出的日志级别
        pass

    # 当前时间str "Y-M-d H:M:S"
    def nowtime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 标准化日志str "[nowtime][level][name][module_name] log"
    def log(self, *values, level: str, module_name: str = None) -> str:
        if module_name:
            module_name = f"[{module_name}]"
        else:
            module_name = ""
        return "\r"+f"[{self.nowtime()}][{level}][{self.name}]{module_name} {' '.join([str(i) for i in [*values]])}".replace("\r","\\r").replace("\n","\\n")

    # info日志
    def info(self, *values, module_name: str = None) -> None:
        if "INFO" in self.loglevel:
            msg = self.log(*values, level="INFO", module_name=module_name)
            print(msg, end = "\n> ")
    
    # debug日志
    def debug(self, *values, module_name: str = None) -> None:
        if "DEBUG" in self.loglevel:
            msg = self.log(*values, level="DEBUG", module_name=module_name)
            print(msg, end="\n> ")
    
    # warn日志 loglevel无"WARN"时raise Exception
    def warn(self, *values, warn: Exception, module_name: str = None) -> None | Exception:
        if "WARN" in self.loglevel:
            warn = self.log(*values, warn, level="WARN", module_name=module_name)
            print(warn, end="\n> ")
        else:
            raise_exception(warn)
    
    # 控制台输入
    def user(self, string):
        print(f"\r{string}", end="\n> ")