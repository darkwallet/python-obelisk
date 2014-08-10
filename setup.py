from setuptools import setup, find_packages

setup(
    name='python-obelisk',
    version="0.1",
    packages=find_packages(exclude="examples"),
    zip_safe=False,
)
