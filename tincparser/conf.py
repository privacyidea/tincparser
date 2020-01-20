# -*- coding: utf-8 -*-

import six
from collections import OrderedDict

from pyparsing import (Word, alphanums, White, CharsNotIn, Optional, Literal, OneOrMore,
                       pythonStyleComment, Group)

FILE_HEADER = """# File parsed and saved by privacyidea.\n"""
RSA_HEADER = '-----BEGIN RSA PUBLIC KEY-----'
RSA_FOOTER = '-----END RSA PUBLIC KEY-----'
OLD_HEADER = '-----BEGIN OLD PUBLIC KEY-----'
OLD_FOOTER = '-----END OLD PUBLIC KEY-----'


class ParserError(RuntimeError):
    pass


class TincConfParser(object):
    key = Word(alphanums)
    maybe_space = Optional(White().suppress())
    value = CharsNotIn("\n")
    config_entry = Group(key +
                         Optional(Literal("=")).suppress() + # = is not required
                         maybe_space +
                         value).setResultsName("entries", True)
    base64word = Word(alphanums + '+/=')
    current_key = Group(Literal(RSA_HEADER) +
                        OneOrMore(base64word) +
                        Literal(RSA_FOOTER)).setResultsName("keys", True)
    old_key = Group(Literal(OLD_HEADER) +
                    OneOrMore(base64word) +
                    Literal(OLD_FOOTER)).setResultsName("old_keys", True)

    conf_file = OneOrMore(config_entry | current_key | old_key).ignore(pythonStyleComment)


class TincConfFile(OrderedDict):
    """
    Parser and Editor for tinc.conf files
    This also handles an embedded RSA public key in the PEM format.
    It is stored in the ``rsa_public_key`` attribute.
    Old public keys are stored in the ``old_public_keys`` attribute.
    """
    def __init__(self, io, filename):
        OrderedDict.__init__(self)
        self.io = io
        self.filename = filename
        self.rsa_public_key = ''
        self.old_public_keys = []
        self._open()

    def _parse(self, f):
        result = TincConfParser.conf_file.parseString(to_unicode(f))
        for entry in result.get("entries", []):
            self[entry[0]] = entry[1]
        keys = result.get("keys", [])
        if keys:
            if len(keys) > 1:
                raise ParserError("Hostfile specifies more than one public key!")
            self.rsa_public_key = '\n'.join(keys[0])
        old_keys = result.get("old_keys", [])
        for old_key in old_keys:
            self.old_public_keys.append('\n'.join(old_key))

    def _generate(self):
        lines = [FILE_HEADER]
        for key, value in self.items():
            lines.append('{} = {}'.format(key, value))
        for old_key in self.old_public_keys:
            lines.extend(['', old_key])
        if self.rsa_public_key:
            lines.extend(['', self.rsa_public_key])
        # Ensure newline at the end of file
        lines.append('')
        return '\n'.join(lines)

    def _open(self):
        self.clear()
        self.rsa_public_key = ''
        self.old_public_keys = []
        if self.io.exists(self.filename):
            with self.io.open(self.filename, 'r') as f:
                self._parse(f.read())

    def save(self):
        with self.io.open(self.filename, 'w') as f:
            f.write(self._generate())


def to_unicode(s, encoding="utf-8"):
    """
    Converts the string s to unicode if it is of type bytes.

    :param s: the string to convert
    :type s: bytes or str
    :param encoding: the encoding to use (default utf8)
    :type encoding: str
    :return: unicode string
    :rtype: str
    """
    if isinstance(s, six.text_type):
        return s
    elif isinstance(s, bytes):
        return s.decode(encoding)
    # TODO: warning? Exception?
    return s
