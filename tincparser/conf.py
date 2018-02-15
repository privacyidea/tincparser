from collections import OrderedDict

FILE_HEADER = """# File parsed and saved by privacyidea.\n"""
RSA_HEADER = '-----BEGIN RSA PUBLIC KEY-----'
RSA_FOOTER = '-----END RSA PUBLIC KEY-----'

class TincConfFile(OrderedDict):
    """
    Parser and Editor for tinc.conf files
    This also handles an embedded RSA public key in the PEM format.
    It is stored in the ``rsa_public_key`` attribute.
    """
    def __init__(self, io, filename):
        OrderedDict.__init__(self)
        self.io = io
        self.filename = filename
        self.rsa_public_key = ''
        self._open()

    def _parse(self, lines):
        items = OrderedDict()
        # boolean flag that determines whether we are currently inside a PEM block
        parsing_rsa_key = False
        rsa_key = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            if line.startswith(RSA_HEADER):
                parsing_rsa_key = True
                rsa_key.append(line)
            elif parsing_rsa_key:
                rsa_key.append(line)
                if line.startswith(RSA_FOOTER):
                    parsing_rsa_key = False
            else:
                key, value = line.split('=')
                items[key.strip()] = value.strip()
        assert not parsing_rsa_key
        return items, '\n'.join(rsa_key)

    def _generate(self):
        lines = [FILE_HEADER]
        for key, value in self.iteritems():
            lines.append('{} = {}'.format(key, value))
        if self.rsa_public_key:
            lines.extend(['', self.rsa_public_key])
        # Ensure newline at the end of file
        lines.append('')
        return '\n'.join(lines)

    def _open(self):
        self.clear()
        if self.io.exists(self.filename):
            with self.io.open(self.filename, 'r') as f:
                values, rsa_key = self._parse(f.readlines())
                self.update(values)
                self.rsa_public_key = rsa_key

    def save(self):
        with self.io.open(self.filename, 'w') as f:
            f.write(self._generate())
