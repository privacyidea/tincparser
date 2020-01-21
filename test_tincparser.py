# -*- coding: utf-8 -*-

from shutil import copyfile
from .tincparser import TincConfFile, LocalIOHandler, UpScript, NetsBoot


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
-----END RSA PUBLIC KEY-----"""


def test_conf_01_read():
    conf = TincConfFile(LocalIOHandler(), 'testdata/tinc.conf')
    assert conf['Name'] == 'pinode1'
    assert conf['Device'] == '/dev/net/tun'
    assert conf.rsa_public_key == ''
    assert conf.old_public_keys == []


def test_conf_02_write(tmp_path):
    tmp_cnf = tmp_path / 'tmp.conf'
    copyfile('testdata/tinc.conf', str(tmp_cnf))
    conf = TincConfFile(LocalIOHandler(), str(tmp_cnf))
    assert conf['Name'] == 'pinode1'
    conf['Hello'] = 'World'
    conf['Device'] = '/dev/net/thunfisch'
    conf.save()
    with tmp_cnf.open() as f:
        contents = f.read()
        assert 'Hello = World' in contents
        assert 'Device = /dev/net/thunfisch\n' in contents
        assert '/dev/net/tun' not in contents
    tmp_cnf.unlink()


def test_conf_03_read_hostfile():
    conf = TincConfFile(LocalIOHandler(), 'testdata/hostfile')
    assert conf['Address'] == '192.168.33.201'
    assert conf.rsa_public_key == RSA_PUBLIC_KEY
    assert conf.old_public_keys == []


def test_conf_04_write_hostfile(tmp_path):
    tmp_hosts = tmp_path / 'hostfile'
    copyfile('testdata/hostfile', str(tmp_hosts))
    conf = TincConfFile(LocalIOHandler(), str(tmp_hosts))
    assert conf['Address'] == '192.168.33.201'
    conf['Address'] = '1.2.3.4'
    conf['Foo'] = 'Bar'
    conf.save()
    with tmp_hosts.open() as f:
        contents = f.read()
        assert 'Address = 1.2.3.4' in contents
        assert 'Foo = Bar' in contents
        assert 'Address = 192.168.33.201' not in contents
        assert RSA_PUBLIC_KEY in contents
    tmp_hosts.unlink()


def test_conf_05_create_file(tmp_path):
    config_file = tmp_path / 'create.conf'
    conf = TincConfFile(LocalIOHandler(), str(config_file))
    assert len(conf) == 0
    assert conf.rsa_public_key == ''
    conf['Hello'] = 'World'
    conf['Key2'] = 'Value2'
    conf.rsa_public_key = RSA_PUBLIC_KEY
    conf.save()
    with config_file.open() as f:
        contents = f.read()
        assert 'Hello = World' in contents
        assert 'Key2 = Value2' in contents
        assert RSA_PUBLIC_KEY in contents
    config_file.unlink()


def test_conf_06_old_public_keys(tmp_path):
    tmp_hosts = tmp_path / 'hosts_old_keys'
    copyfile('testdata/hostfile_with_old_key', str(tmp_hosts))
    conf = TincConfFile(LocalIOHandler(), str(tmp_hosts))
    assert conf['Address'] == '192.168.33.201'
    assert conf['Subnet'] == '172.20.1.1'
    assert conf['Another'] == 'Key'
    assert conf.rsa_public_key == """-----BEGIN RSA PUBLIC KEY-----
MIICCgKCAgEAzLzKCxbeBpekdY3Xi7eT0ryZUv+261aYUqWdZQCNMutOtyIgIbdq
ttP2i9J4PirfwUiLQtTA6+3gfLpl0SYnZz/XdZS5tRMEmgZrBb572kUL/5hwbEdW
JNF58Ca9YmlPc0P2rpaSs7nhDN/XtnYQJvET+uAk+Rs2pwCuJxW5odj7zeAYRHTu
H2LX12Xb5alCqX4DZkrf9Eqyal0htRdQM/Oa3OvkRBeGezQCy7qxtANHyJVBFdOC
/FAgoxEcDmAZPtW8A5yKO/2AaPiRfDISgSV8rJ9d/QBzg4jwxPD6+3Cn2ZfdIRdC
YWfacFQ04rAdUjF3hD4/y7HIOyDkXVsdBkpUSGLtmUKKsqXaiREmjf6I9Geejj3P
IjaT0JbeJQ0s6FcA9O0CFH9ezxXJSnLlLVTAsibpCfgxMFc4pA19NyK4bG1aqnk3
ngDzn7Djwc6PPOwrhZjrjiM1lSdEkaCQwy8s7LaZbRViaJXFDg0pl/ZCdB2rW0wb
ooNxX6bmyE5ENDBe1MDP6MUWRCG9aEn/DUxdN9jbNsejqveHd9//+ozXGXK/TGtR
8Wn1ibUdZqAsUjKFhA4eVh9083AtmrAVbvTSJzx+EmikUn6zyGzIJydvf9DcIsRS
bvHK/BneL4ITkO3dDjfl+G9chBkuqNXSS7V37FdRMCBQJLy4TK2l5zMCAwEAAQ==
-----END RSA PUBLIC KEY-----"""
    assert conf.old_public_keys == ["""-----BEGIN OLD PUBLIC KEY-----
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
-----END OLD PUBLIC KEY-----""", """-----BEGIN OLD PUBLIC KEY-----
ABCDEgKCAgEAob52Pto+hmEnVZHr5ti7MM8FFjj9A5ajuO/VoHGh6GlWVj1yOJcH
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
-----END OLD PUBLIC KEY-----"""]
    conf['Bar'] = 'Cdr'
    del conf.old_public_keys[0]
    conf.save()
    with tmp_hosts.open() as f:
        contents = f.read()
        assert "Bar = Cdr" in contents
        assert "-----BEGIN OLD PUBLIC KEY-----\nABCDEg" in contents
        assert "-----BEGIN OLD PUBLIC KEY-----\nMIICCg" not in contents
    tmp_hosts.unlink()


def test_tincup_01_read():
    script = UpScript(LocalIOHandler(), 'testdata/tinc-up')
    assert script.prolog == [
        '#!/bin/sh',
        'echo "hello world"'
    ]
    assert script.appliance_section == [
        'ip link set $INTERFACE up',
        'ip addr add 172.20.1.1 dev $INTERFACE',
        'ip route add 172.20.1.0/30 dev $INTERFACE'
    ]
    assert script.epilog == [
        'echo "good bye world"',
        'exit 0'
    ]


def test_tincup_02_modify(tmp_path):
    tmp_upfile = tmp_path / 'tinc-up'
    copyfile('testdata/tinc-up', str(tmp_upfile))
    script = UpScript(LocalIOHandler(), str(tmp_upfile))
    script.prolog.append('#comment')
    script.appliance_section = [
        'echo "hello"',
        'echo "world!"'
    ]
    script.epilog = ['exit 1']
    script.save()
    with tmp_upfile.open() as f:
        assert f.read().split('\n') == [
            '#!/bin/sh',
            'echo "hello world"',
            '#comment',
            '# BEGIN AUTOGENERATED',
            'echo "hello"',
            'echo "world!"',
            '# END AUTOGENERATED',
            'exit 1',
            ''
        ]
    tmp_upfile.unlink()


def test_tincup_03_from_scratch(tmp_path):
    tmp_upfile = tmp_path / 'tinc-up2'
    script = UpScript(LocalIOHandler(), str(tmp_upfile))
    script.appliance_section = ['echo hi']
    script.save()
    with tmp_upfile.open() as f:
        assert f.read().split('\n') == [
            '#!/bin/sh',
            '# BEGIN AUTOGENERATED',
            'echo hi',
            '# END AUTOGENERATED',
            ''
        ]
    tmp_upfile.unlink()


def test_netsboot_01_read():
    nets = NetsBoot(LocalIOHandler(), 'testdata/nets.boot')
    assert nets.nets == ['privacyideaVPN']


def test_netsboot_02_modify(tmp_path):
    tmp_nets = tmp_path / 'nets.boot'
    copyfile('testdata/nets.boot', str(tmp_nets))
    nets = NetsBoot(LocalIOHandler(), str(tmp_nets))
    nets.add('foo')
    nets.add('privacyideaVPN')
    nets.save()
    with tmp_nets.open() as f:
        assert f.read().split('\n') == [
            '## This file contains all names of the networks to be started on '
            'system startup.',
            'privacyideaVPN',
            'foo',
            ''
        ]
    tmp_nets.unlink()
