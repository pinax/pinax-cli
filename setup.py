from setuptools import find_packages, setup

VERSION = "1.1.0"
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


Supported Python Versions
-------------------------

``pinax-cli`` supports Python 2.7, 3.4, 3.5, and 3.6

"""

setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="a command line interface for Pinax",
    name="pinax-cli",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-cli/",
    license="MIT",
    py_modules=["pcli"],
    install_requires=[
        "click>=6.7",
        "colorama>=0.3.9"
        "requests>=2.18.4",
    ],
    entry_points="""
        [console_scripts]
        pinax=pcli:main
    """,
    classifiers=[
        "Development Status :: 5 - Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
