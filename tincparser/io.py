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

    def makedirs(self, dirname):
        """
        Recursively create a dictionary. Caveat: If the directory already exists, this does not throw an error!
        """
        raise NotImplementedError()

    def chmod(self, filename, mode):
        raise NotImplementedError()


class LocalIOHandler(IOHandler):
    def open(self, filename, mode):
        return open(filename, mode)

    def exists(self, filename):
        return os.path.exists(filename)

    def makedirs(self, dirname):
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def chmod(self, filename, mode):
        os.chmod(filename, mode)


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

    def makedirs(self, dirname):
        try:
            self.sftp.listdir(dirname)
        except IOError:
            parent_dirname, _ = os.path.split(dirname.rstrip('/'))
            self.makedirs(parent_dirname)
            self.sftp.mkdir(dirname)

    def chmod(self, filename, mode):
        self.sftp.chmod(filename, mode)