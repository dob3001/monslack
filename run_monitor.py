#!/usr/bin/python
from daemon import runner

from monslack.monitor import MonSlack

def run_monitor():
    ms = MonSlack()
    drun = runner.DaemonRunner(ms)
    drun.do_action()


if __name__ == "__main__":
    run_monitor()
