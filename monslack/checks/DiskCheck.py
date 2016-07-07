import os
from collections import namedtuple

class DiskCheck(object):

    def __init__(self, config):
        self.config = config

    def check(self, path):
        message = False
        text = None
        (total, used, free) = self._disk_usage(path)
        if free < self.config["diskwarnlvl"]:
            message = True
            text = "Disk %s has only %sMB free, we need to do something!" % (path, ((free / 1024) / 1024))
        return (message, text)

    def _disk_usage(self, path):
        _ntuple_diskusage = namedtuple('usage', 'total used free')
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return _ntuple_diskusage(total, used, free)



