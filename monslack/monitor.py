#!/usr/bin/python

import json
import os
import sys
import time
import requests
import psutil
from monslack.checks.DiskCheck import DiskCheck
from monslack.checks.CPUCheck import CPUCheck
from monslack.checks.MemoryCheck import MemoryCheck
from monslack.checks.LogCheck import LogCheck

class MonSlack():

    def __init__(self):
        self.config = self._load_config()
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/monslack.pid'
        self.pidfile_timeout = 5
        self.disk = False
        self.cpu = False
        self.memory = False
        self.log = False

        if self.config["checks"]["disk"]:
            self.disk = DiskCheck(self.config)
        if self.config["checks"]["cpu"]:
            self.cpu = CPUCheck(self.config)
        if self.config["checks"]["cpu"]:
            self.memory = MemoryCheck(self.config)
        if self.config["checks"]["log"]:
            self.log = LogCheck(self.config)



    def _load_config(self, config="/etc/monslack/config.json"):
        """
        _load_config Function, read in the local json config file
        Inputs:
        Outputs: data structure
        """
        data = {}
        try:
            with open(config, "r") as monsconf:
                data = json.load(monsconf)

        except Exception as exceptme:
            print exceptme
            print "Failed to open %s" % config
            sys.exit()

        return data


    def _send_slack_error(self, text):
        payload = self.config["webhook"]
        if "hostname" in self.config:
            hostname = self.config['hostname']
        else:
            hostname = os.uname()[1]

        payload['text'] = "%s: %s" % (hostname, text)
        res = requests.post(self.config["webhookurl"], data=json.dumps(payload))
        return res.text


    def run(self):
        while True:
            if self.disk:
                for path in self.config["diskpaths"]:
                    (message, text) = self.disk.check(path)
                    if message:
                        self._send_slack_error(text)
 
            if self.cpu:
                (message, text) = self.cpu.check()
                if message:
                    self._send_slack_error(text)
 
            if self.memory:
                (message, text) = self.memory.check()
                if message:
                    self._send_slack_error(text)

            if self.log:
                for log in self.config["logs"]:
                    (message, text) = self.log.check(log)
                    if message:
                        self._send_slack_error(text)

            time.sleep(self.config["interval"])

