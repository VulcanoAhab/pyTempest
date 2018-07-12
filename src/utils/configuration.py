import yaml

class Job:
    """
    """
    def __init__(self, configFile):
        """
        """
        self.file=configFile

    def load(self):
        """
        """
        fd=open(self.file, "r")
        cfg=yaml.load(fd)
        fd.close()
        for key,values in cfg.items():
            setattr(self, key, values)
