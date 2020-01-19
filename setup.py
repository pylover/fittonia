import os.path
import re

from setuptools import setup


# reading package's version (same way sqlalchemy does)
with open(
    os.path.join(os.path.dirname(__file__), 'fittonia.py')
) as v_file:
    package_version = \
        re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read())\
        .group(1)


dependencies = [
    'yhttp-pony >= 1.1.2, < 2',
    'yhttp-auth >= 1.1.1, < 2',
]


setup(
    name='fittonia',
    version=package_version,
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    url='http://github.com/pylover/fittonia',
    description='Store, Update and get JSON document using URL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    install_requires=dependencies,
    py_modules=['fittonia'],
    entry_points=dict(console_scripts='fittonia=fittonia:app.climain'),
    license='MIT',
)

