from setuptools import setup, find_namespace_packages

setup(
    name='pyrsched-cli',
    packages=find_namespace_packages(include=['pyrsched.*']),
    install_requires=['rpyc',]
)