from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt and as well as configure
# dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]

dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name='ciphersa',
    description='A simple commandline app for encrypting and decrypting your files',
    version='1.0.0',
    py_modules=['ciphersa'],
    packages=find_packages(),  # list of all packages
    install_requires=install_requires,
    python_requires='>=3.8',  # any python greater than 3.8
    entry_points='''
        [console_scripts]
        ciphersa=ciphersa:main
    ''',
    author="Jan Korcek",
    keyword="cipher, encryption, decryption, rsa",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/korcekj/ciphersa.git',
    download_url='https://github.com/korcekj/ciphersa.git/archive/master.zip',
    dependency_links=dependency_links,
    author_email='xkorcek@stuba.sk',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ]
)
