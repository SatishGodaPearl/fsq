from distutils.core import setup
from glob import glob

setup(
    name='fsq',
    version='0.2.3',
    author='Matthew Story',
    author_email='matt.story@axial.net',
    packages=['fsq', 'fsq.tests', 'fsq.remote', ],
    scripts=['bin/fsq'],
    data_files=[('share/man/man1', ['man/man1/fsq.1',
                                    'man/man1/fsq-down.1',
                                    'man/man1/fsq-enqueue.1',
                                    'man/man1/fsq-scan.1',
                                    'man/man1/fsq-up.1',
                                    'man/man1/fsq-rm-host.1',
                                    'man/man1/fsq-add-host.1',
                                    'man/man1/fsq-down-host.1',
                                    'man/man1/fsq-up-host.1',
                                    'man/man1/fsq-install.1']),
                ('share/man/man7', ['man/man7/fsq.7']),
                ('libexec/fsq', ['libexec/fsq/down.py',
                                 'libexec/fsq/enqueue.py',
                                 'libexec/fsq/install.py',
                                 'libexec/fsq/scan.py',
                                 'libexec/fsq/up.py',
                                 'libexec/fsq/add-host.py',
                                 'libexec/fsq/down-host.py',
                                 'libexec/fsq/host-dist.py',
                                 'libexec/fsq/push.py',
                                 'libexec/fsq/rm-host.py',
                                 'libexec/fsq/up-host.py',
                                 'libexec/fsq/jsonrpcd.py',
                                 ]),
               ],
    url='https://github.com/axialmarket/fsq',
    license='3-BSD',
    description='File System Queue',
    long_description=open('./README.rst').read(),
    requires= ['jsonrpclib']
)

