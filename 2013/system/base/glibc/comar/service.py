
from comar.service import *

serviceType = "local"
serviceConf = "glibc"
serviceDefault = "conditional"

serviceDesc = _({"en": "Glibc",
                 "tr": "Glibc"})

@synchronized
def start():
    startService(command="/usr/sbin/glibc",
                 args = config.get("args", "destroy"),
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/glibc",
                donotify=True)

def ready():
    import os
    status = is_on()
    if status == "on" or (status == "conditional" and os.path.exists("/sys/coffee/ready")):
        start()

def status():
    return checkDaemon("/var/run/glibc.pid")

