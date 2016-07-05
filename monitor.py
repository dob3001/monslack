#!/usr/bin/python

import json
import os
import sys
import time
import requests
import psutil
import daemon
from collections import namedtuple

def _disk_usage(path):
    _ntuple_diskusage = namedtuple('usage', 'total used free')
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total, used, free)

def _send_slack_error(config, message):
    payload = config["webhook"]
    if "hostname" in config:
        hostname = config['hostname']
    else:
        hostname = os.uname()[1]

    payload['text'] = "%s: %s" % (hostname, message)
    res = requests.post(config["webhookurl"], data=json.dumps(payload))
    print res.text

def _check_for_errors(config):
    ERRORSEEN = _load_data()
    for log in config["logs"]:
        with open(log) as f:
            lines = f.readlines()
        f.close()
        for line in lines:
            for errorstring in config["errorstrings"]:
                if errorstring in line:
                    items = line.split(" ")
                    #This needs to be better!
                    key = "%s-%s" % (items[0], items[1])
                    value = "%s" % (' '.join(items[4:]))
                    if key not in ERRORSEEN:
                        print "Seen at %s the error: %s" % (key, value)
                        ERRORSEEN[key] = value
                        _send_slack_error(config, value)

    for disk in config["diskpaths"]:
        (total, used, free) = _disk_usage(disk)
        if free < config["diskwarnlvl"]:
            _send_slack_error(config, "Disk %s has only %sMB free, we need to do something!" % (disk, ((free / 1024) / 1024)))

    #p = psutil.Process(os.getpid())
    #cpuusage = p.get_cpu_percent(interval=0)
    meminfo = psutil.virtual_memory()

    loadavg = _read_loadavg().split(" ")
    if int(round(float(loadavg[0]))) > config["cpuwarnlevel"]:
        _send_slack_error(config, "CPU is being used up, we may need to do something!")
    if int(meminfo.free) < config["memoryfree"]:
        _send_slack_error(config, "System Memory only has %sMB free, we may need to do something!" % ((int(meminfo.free) / 1024) / 1024))
    _save_data(ERRORSEEN)

def _read_loadavg():
    lavg = open("/proc/loadavg", "r")
    lavgline = lavg.readline()
    lavg.close()
    return lavgline

def _save_data(data):
    """
    _savedata Function, save data structure to file as json
    Inputs: dict
    Outputs:
    """

    with open(".data", "w") as dbapif:
        dbapif.write(json.dumps(data, indent=2))
    dbapif.close()

def _load_config(config="/etc/monslack/config.json"):
    """
    _loadconfig Function, read in the local json config file
    Inputs:
    Outputs: data structure
    """
    data = {}
    try:
        with open(config, "r") as monsconf:
            data = json.load(monsconf)

    except:
        print "Failed to open %s" % config
        sys.exit()

    return data



def _load_data():
    """
    _loaddata Function, read in the local json data file
    Inputs:
    Outputs: data structure
    """
    data = {}
    try:
        with open(".data", "r") as dbapif:
            data = json.load(dbapif)

    except:
        #Catch the real exception
        with open(".data", "w") as dbapif:
            dbapif.write(json.dumps(data))
        dbapif.close()
    return data



configdata = _load_config()

with daemon.DaemonContext():
    _check_for_errors(configdata)
    time.sleep(configdata["interval"])

