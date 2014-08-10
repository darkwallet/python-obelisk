from setuptools import setup, find_packages

setup(
    name='python-obelisk',
    version="0.1.2",
    install_requires=['ecdsa', 'pyzmq'],
    maintainer='Dionysis Zindros',
    maintainer_email='dionyziz@gmail.com',
    zip_safe=False,
    description="Python native client for the obelisk blockchain server.",
    long_description=open('README.txt').read(),
    license='GNU Affero General Public License',
    keywords='bitcoin blockchain obelisk obeliskoflight query transaction federated',
    url='https://github.com/darkwallet/python-obelisk'
)
