import os

import yaml


class LoadConfig:
    def __init__(self, filename):
        """Constructor of `LoadConfig`
        
        Args:
            filename (:obj:`str`): absoulte path of the file to be loaded.
     
        Returns:
            None
        """
        self._file = filename

    def load(self):
        """read yaml files into a dict object

        Raises:
            IOError: if file does not exists
        """
        if not os.path.isfile(self._file):
            raise IOError("{} file does not exist".format(self._file))

        with open(self._file, "r") as f:
            self._conf = yaml.safe_load(f.read())

        return self._conf
