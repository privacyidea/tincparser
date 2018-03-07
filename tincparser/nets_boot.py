class NetsBoot(object):
    """
    Extremely simple parser for /etc/tinc/nets.boot
    This simply reads all lines into a list (this also includes comments).
    Adding a network via ``add`` avoids duplicate entries.
    """
    def __init__(self, io, filename):
        self.io = io
        self.filename = filename
        self._clear()
        self._open()

    def _clear(self):
        self.lines = []

    def _open(self):
        self._clear()
        if self.io.exists(self.filename):
            with self.io.open(self.filename, 'r') as f:
                for line in f.readlines():
                    self.lines.append(line.strip())

    def _generate(self):
        return '\n'.join(self.lines)

    def add(self, net):
        if net not in self.lines:
            self.lines.append(net)

    @property
    def nets(self):
        """ Return all network names, i.e. all lines excluding blank lines and lines starting with '#' """
        return [line for line in self.lines if line and not line.startswith('#')]

    def save(self):
        with self.io.open(self.filename, 'w') as f:
            f.write(self._generate())
            f.write('\n')
