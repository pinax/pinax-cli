import codecs

from os import path
from setuptools import setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    author="Pinax Developers",
    author_email="developers@pinaxproject.com",
    description="a command line for Pinax",
    name="pinax-cli",
    long_description=read("README.rst"),
    version="1.0.0",
    url="http://github.com/pinax/pinax-cli/",
    license="MIT",
    py_modules=["pcli"],
    install_requires=[
        "Click==5.1",
        "requests==2.7.0",
        "colorama==0.3.3"
    ],
    entry_points="""
        [console_scripts]
        pinax=pcli:main
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
