import codecs
import os.path
from setuptools import find_packages, setup

NAME = 'sqlalchemy_serializable'
with codecs.open(os.path.join(NAME, 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

requires = [
    'sqlalchemy',
    'mapping_extend'
]

setup(
    name=NAME,
    version=version,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    author='Brendan Zerr',
    author_email='bzerr@brainwire.ca',
    description='SQLAlchemy model-to-JSON, following Pyramid __json__ API',
    long_description=long_description,
    url='',
    install_requires=requires,
    tests_require=requires,
    license='MIT',
    classifiers=[]
)
