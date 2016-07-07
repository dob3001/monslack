
class CPUCheck(object):

    def __init__(self, config):
        self.config = config

    def check(self):
        message = False
        text = None
        loadavg = self._read_loadavg().split(" ")
        if int(round(float(loadavg[0]))) > self.config["cpuwarnlevel"]:
            message = True
            text = "Disk %s has only %sMB free, we need to do something!" % (path, ((free / 1024) / 1024))    
        return (message, text)       

    def _read_loadavg(self):
        lavg = open("/proc/loadavg", "r")
        lavgline = lavg.readline()
        lavg.close()
        return lavgline

