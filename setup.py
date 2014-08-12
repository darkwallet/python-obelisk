from setuptools import setup

setup(
    name='python-obelisk',
    version="0.1.3",
    install_requires=['twisted', 'ecdsa', 'pyzmq'],
    packages=['obelisk'],
    maintainer='Dionysis Zindros',
    maintainer_email='dionyziz@gmail.com',
    zip_safe=False,
    description="Python native client for the obelisk blockchain server.",
    long_description=open('README.txt').read(),
    license='GNU Affero General Public License',
    keywords='bitcoin blockchain obelisk obeliskoflight query transaction federated',
    url='https://github.com/darkwallet/python-obelisk'
)
