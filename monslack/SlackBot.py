from slackclient import SlackClient
import subprocess
import time

class SlackBot(object):

    def __init__(self, config):
        self.config = config
        self.lastcheck = time.time()
        self._send_message("%s has connected and is monitoring host: %s" % (self.config["bot"]["name"], self.config["hostname"]))

    def check(self):
        sc = SlackClient(self.config["bot"]["token"])
        history = sc.api_call("channels.history", channel=self.config["bot"]["channel"], oldest=self.lastcheck )
        botname = "%s" % self.config["bot"]["name"]
        for message in history["messages"]:
            if botname in message["text"]:
                timestamp = message["ts"]
                command = message["text"].split(" ")
                if command[1] == self.config["hostname"]:
                    if command[2] == "df":
                        self._action_df()    
                        self._set_lastcheck(timestamp)
                    elif command[2] == "mem":
                        self._action_mem()
                        self._set_lastcheck(timestamp)
                    elif command[2] == "top":
                        self._action_top()
                        self._set_lastcheck(timestamp)
                    else:
                        self._send_message("I don't know what this action is '%s'. Supported actions: df, mem, top" % command[2])
                        sc.api_call("chat.postMessage", as_user="true:", channel=self.config["bot"]["channel"], text="I don't know what this action is '%s'. Supported actions: df, mem, top" % command[2])
                        self._set_lastcheck(timestamp)
                elif command[1] == "rollcall":
                    self._send_message("%s on %s reporting in" % (self.config["bot"]["name"], self.config["hostname"]))    

    def _set_lastcheck(self, timestamp):
        self.lastcheck = timestamp

    def _action_df(self):
        rdf = subprocess.Popen(["df"], stdout=subprocess.PIPE)
        odf = rdf.communicate()[0]
        self._send_message(odf)        

    def _action_mem(self):
        rmem = subprocess.Popen(["free"], stdout=subprocess.PIPE)
        omem = rmem.communicate()[0]
        self._send_message(omem)

    def _action_top(self):
        rtop = subprocess.Popen(["cat","/proc/loadavg"], stdout=subprocess.PIPE)
        otop = rtop.communicate()[0]
        self._send_message(otop)

    def _send_message(self, message):
        sc = SlackClient(self.config["bot"]["token"])
        sc.api_call("chat.postMessage", as_user="true:", channel=self.config["bot"]["channel"], text=message)

