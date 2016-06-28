import pickle
import logging

log = logging.getLogger(__name__)


class PickledContext:
    def __init__(self, cls, path):
        self.path = path
        self._cls = cls
        self.obj = None

    def __enter__(self):
        obj = None
        try:
            with open(self.path, 'rb') as input:
                self.obj = pickle.load(input)
        except IOError:
            log.warning("Path {0} not found. Creating a new {1} instance".format(self.path, self._cls.__name__))
            self.obj = self._cls()
        return self.obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            with open(self.path, 'wb') as output:
                pickle.dump(self.obj, output)
                log.info("Saving {} to {}".format(self.obj.__class__.__name__, self.path))
        return False
