from collections import OrderedDict

FILE_HEADER = """# File parsed and saved by privacyidea.\n"""


class TincConfFile(OrderedDict):
    """
    Parser and Editor for tinc.conf files
    """
    def __init__(self, io, filename):
        OrderedDict.__init__(self)
        self.io = io
        self.filename = filename
        self._open()

    def _parse(self, lines):
        items = OrderedDict()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            key, value = line.split('=')
            items[key.strip()] = value.strip()
        return items

    def _generate(self):
        lines = [FILE_HEADER]
        for key, value in self.iteritems():
            lines.append('{} = {}'.format(key, value))
        return '\n'.join(lines)

    def _open(self):
        self.clear()
        if self.io.exists(self.filename):
            with self.io.open(self.filename, 'r') as f:
                self.update(self._parse(f.readlines()))

    def save(self):
        with self.io.open(self.filename, 'w') as f:
            f.write(self._generate())
