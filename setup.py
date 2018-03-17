import os
import sys
from setuptools import setup

VERSION = "1.1.3"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-blank.svg
    :target: https://pypi.python.org/pypi/pinax-cli/

============================
Pinax Command Line Interface
============================

.. image:: https://img.shields.io/pypi/v/pinax-cli.svg
    :target: https://pypi.python.org/pypi/pinax-cli/

\ 

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-cli.svg
    :target: https://circleci.com/gh/pinax/pinax-cli
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-cli.svg
    :target: https://codecov.io/gh/pinax/pinax-cli
.. image:: https://img.shields.io/github/contributors/pinax/pinax-cli.svg
    :target: https://github.com/pinax/pinax-cli/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-cli.svg
    :target: https://github.com/pinax/pinax-cli/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-cli.svg
    :target: https://github.com/pinax/pinax-cli/pulls?q=is%3Apr+is%3Aclosed

\ 

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://pypi.python.org/pypi/pinax-cli/

\ 

``pinax-cli`` is a command-line interface for installing Pinax starter projects,
and learning more about available Pinax apps.


Supported Django and Python Versions
------------------------------------

pinax-cli creates projects using Python v3.4+ and Django v2.0+

"""

# Check for valid Python.
if sys.version_info < (3, 4, 0):
    print("Python {} is installed, but pinax-cli requires Python 3.4 or greater for compatibility with Django v2.x".format(sys.version.split()[0]))
    sys.exit()


# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()


setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="a command line interface for Pinax",
    name="pinax-cli",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-cli/",
    packages=["pinaxcli"],
    license="MIT",
    install_requires=[
        "click>=6.7",
        "crayons>=0.1.2",
        "django>=2.0",
        "requests>=2.18.4",
    ],
    entry_points={
        "console_scripts": [
            "pinax = pinaxcli.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
