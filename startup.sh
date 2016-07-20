#!/bin/bash
rm -f /var/run/monslack.pid
cd /opt/;/usr/bin/python run_monitor.py start
