from setuptools import find_packages
from distutils.core import setup

setup(
    name='ergaleia',
    version='1.3.1',
    packages=find_packages(exclude=['tests']),
    description='A library of random tools',
    long_description="""
Documentation
-------------
    You can see the project and documentation at the `GitHub repo <https://github.com/robertchase/ergaleia>`_
    """,
    author='Bob Chase',
    url='https://github.com/robertchase/ergaleia',
    license='MIT',
)
