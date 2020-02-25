import pickle
import json
import logging

log = logging.getLogger(__name__)


class pickled_context:
    def __init__(self, cls, path):
        self.path = path
        self._cls = cls
        try:
            with open(self.path, 'rb') as input:
                self.obj = pickle.load(input)
        except IOError:
            log.warning("Path {0} not found. Creating a new {1} instance".format(self.path,
                                                                                 self._cls.__name__))
            self.obj = self._cls()

    def __enter__(self):
        return self.obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None or exc_type == SystemExit:
            with open(self.path, 'wb') as output:
                pickle.dump(self.obj, output)
                log.info("Saving {} to {}".format(self.obj.__class__.__name__, self.path))
        return False


class json_context:
    def __init__(self, cls, path):
        self.path = path
        self._cls = cls
        try:
            with open(self.path, 'r') as input:
                data = json.load(input)
                self.obj = self._cls.from_dict(data)
        except IOError:
            log.warning("Path {0} not found. Creating a new {1} instance".format(self.path, self._cls.__name__))
            self.obj = self._cls()

    def __enter__(self):
        return self.obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None or exc_type == SystemExit:
            with open(self.path, 'w') as output:
                json.dump(self.obj.to_dict(), output, indent=2)
                log.info("Saving {} to {}".format(self.obj.__class__.__name__, self.path))
        return False
