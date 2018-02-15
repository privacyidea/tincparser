import os


class IOHandler(object):
    """
    Abstract base class for file I/O. By using this, we can use the same code locally
    and remotely (via SFTP).
    """
    def __init__(self):
        pass

    def open(self, filename, mode):
        raise NotImplementedError()

    def exists(self, filename):
        raise NotImplementedError()

class LocalIOHandler(IOHandler):
    def open(self, filename, mode):
        return open(filename, mode)

    def exists(self, filename):
        return os.path.exists(filename)