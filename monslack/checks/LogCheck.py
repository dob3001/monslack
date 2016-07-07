import json

class LogCheck(object):

    def __init__(self, config):
        self.config = config
        
    def check(self, logfile):
        message = False
        text = None

        data = self._load_data()
        with open(logfile) as f:
            lines = f.readlines()
        f.close()
        for line in lines:
            for check in self.config['errorstrings']:
                if check in line:
                    items = line.split(" ")
                    key = "%s-%s" % (items[0], items[1])
                    value = "%s" % (' '.join(items[4:]))
                    if not self._check_data(data, key):
                        message = True
                        text += "Seen at %s the error: %s\n" % (key, value)
        return (message, text)       

    def _check_data(self, data, key):
        if key in data:
            return True

    def _save_data(self, data):
        """
        _savedata Function, save data structure to file as json
        Inputs: dict
        Outputs:
        """

        with open(".data", "w") as dbapif:
            dbapif.write(json.dumps(data, indent=2))
        dbapif.close()

    def _load_data(self):
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

