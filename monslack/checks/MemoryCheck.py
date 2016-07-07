import psutil

class MemoryCheck(object):

    def __init__(self, config):
        self.config = config

    def check(self):
        message = False
        text = None
        meminfo = psutil.virtual_memory()
        if int(meminfo.free) < self.config["memoryfree"]:
            message = True
            text = "System Memory only has %sMB free, we may need to do something!" % ((int(meminfo.free) / 1024) / 1024)
        return (message, text)

