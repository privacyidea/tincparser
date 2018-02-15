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


class SFTPIOHandler(IOHandler):
    """
    IO handler that works remotely via paramiko+SFTP
    """
    def __init__(self, sftp):
        IOHandler.__init__(self)
        self.sftp = sftp

    def open(self, filename, mode):
        return self.sftp.file(filename, mode)

    def exists(self, filename):
        try:
            self.sftp.stat(filename)
            return True
        except IOError:
            return False
