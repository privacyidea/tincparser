import unittest

import os

from tincparser import TincConfFile, LocalIOHandler


RSA_PUBLIC_KEY = """-----BEGIN RSA PUBLIC KEY-----
MIICCgKCAgEAob52Pto+hmEnVZHr5ti7MM8FFjj9A5ajuO/VoHGh6GlWVj1yOJcH
bDq+0JTVeJ/p7Ar6Z5FqHVTghYl65sQ5kXLrVSd7T7njqCjhg+eXBXk7/XZuG74E
keuHB7t5uvR8JVjPpryA49cB5AIKz4OXs08FgUz8CF2s2KmdWMiahBWlhEYMM5Q7
Yo8sjmMXN7inepr/KSHdXFYEitIPjcLKyJfRBxPAUfKnqLI1IvUWzB0ZPNQS1nME
OKoa9XvGaJcb6Qfe0UJqDj/61JCQ5uwspJUY9WUc36SoIDUeH+b1I1gWiTX65tlA
n+Hn8eDojuHJqa7ByLSibHUxXNGXu1h43A8arkmXqTIjgI9cUf7gGWGRXkSwD7t1
CAjjat1135evwXPE0fFzfUcAKqPc6oP2bORgcem7Fc9Osu1YkyJX9t15X1SBP3x/
i07L49Lu8Cf8a5iK/B1Wxd/6vQMvk4XX/DVxkxu79vnu+1D236n05pdKpedUlhC7
rymC8994x9QiYC0hfz3bAbaufEOQw6VV/hXX7e1cXdxTOa/H2gV2FmvUBQC8LwiT
d6PCRRkfkNV3iy6Je2M3DRFnIXUGvxqZvtYw1oqTSJ6GKeAO+pI59XCmMMGQcVtq
rpXDmj21wrjv8Qk3XqqK2PoLwAt4ZuF5EFjLeImhIVQz3gQ90qmj9hcCAwEAAQ==
-----END RSA PUBLIC KEY-----
"""


class TestConf(unittest.TestCase):
    def test_01_read(self):
        conf = TincConfFile(LocalIOHandler(), 'testdata/tinc.conf')
        self.assertEqual(conf['Name'], 'pinode1')
        self.assertEqual(conf['Device'], '/dev/net/tun')
        self.assertEqual(conf.rsa_public_key, '')

    def test_02_write(self):
        conf = TincConfFile(LocalIOHandler(), 'testdata/tinc.conf')
        self.assertEqual(conf['Name'], 'pinode1')
        conf['Hello'] = 'World'
        conf['Device'] = '/dev/net/thunfisch'
        conf.save()
        with open('testdata/tinc.conf') as f:
            contents = f.read()
            self.assertIn('Hello = World', contents)
            self.assertIn('Device = /dev/net/thunfisch\n', contents)
            self.assertNotIn('/dev/net/tun', contents)

    def test_03_read_hostfile(self):
        conf = TincConfFile(LocalIOHandler(), 'testdata/hostfile')
        self.assertEqual(conf['Address'], '192.168.33.201')
        self.assertEqual(conf.rsa_public_key, RSA_PUBLIC_KEY)

    def test_04_write_hostfile(self):
        conf = TincConfFile(LocalIOHandler(), 'testdata/hostfile')
        self.assertEqual(conf['Address'], '192.168.33.201')
        conf['Address'] = '1.2.3.4'
        conf['Foo'] = 'Bar'
        conf.save()
        with open('testdata/hostfile') as f:
            contents = f.read()
            self.assertIn('Address = 1.2.3.4', contents)
            self.assertIn('Foo = Bar', contents)
            self.assertNotIn('Address = 192.168.33.201', contents)
            self.assertIn(RSA_PUBLIC_KEY, contents)

    def test_05_create_file(self):
        config_file = 'testdata/create.conf'
        if os.path.exists(config_file):
            os.remove(config_file)
        conf = TincConfFile(LocalIOHandler(), config_file)
        self.assertEqual(conf.items(), [])
        self.assertEqual(conf.rsa_public_key, '')
        conf['Hello'] = 'World'
        conf['Key2'] = 'Value2'
        conf.rsa_public_key = RSA_PUBLIC_KEY
        conf.save()
        with open(config_file) as f:
            contents = f.read()
            self.assertIn('Hello = World', contents)
            self.assertIn('Key2 = Value2', contents)
            self.assertIn(RSA_PUBLIC_KEY, contents)