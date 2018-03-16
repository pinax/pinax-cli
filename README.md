![](http://pinaxproject.com/pinax-design/patches/pinax-cli.svg)

# Pinax Command Line Interface

[![](https://img.shields.io/pypi/v/pinax-cli.svg)](https://pypi.python.org/pypi/pinax-cli/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-cli.svg)](https://circleci.com/gh/pinax/pinax-cli)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-cli.svg)](https://codecov.io/gh/pinax/pinax-cli)
[![](https://img.shields.io/github/contributors/pinax/pinax-cli.svg)](https://github.com/pinax/pinax-cli/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-cli.svg)](https://github.com/pinax/pinax-cli/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-cli.svg)](https://github.com/pinax/pinax-cli/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Overview](#overview)
  * [Supported Django and Python versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
* [Change Log](#change-log)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable
Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## pinax-cli

### Overview

`pinax-cli` is a command-line interface for installing Pinax starter projects
and learning more about the latest Pinax app releases.

#### Supported Django and Python versions

pinax-cli creates projects using Python v3.4+ and Django v2.0+


## Documentation

### Installation

To install pinax-cli:

```shell
$ pip install pinax-cli
```

### Usage

Invoke pinax-cli with `$ pinax <cmd>` using one of the following commands:

#### `pinax apps`

Show a list of Pinax apps with their release version in the latest Pinax distribution.

```shell
$ pinax apps
```

#### `pinax demos`

Show a list of Pinax demonstration projects with their release version in the latest Pinax distribution.

```shell
$ pinax demos
```

#### `pinax projects`

Show a list of Pinax starter projects and their release version in the latest Pinax distribution.

```shell
$ pinax projects
Release Project
------- ---------------
  4.0.0 account
  4.0.0 blog
  2.0.0 company
        documents
        social-auth
  4.0.0 static
  4.0.0 stripe
        team-wiki
  3.0.0 waitinglist
        wiki
  4.0.0 zero
```

#### `pinax tools`

Show a list of Pinax tools with their release version in the latest Pinax distribution.

```shell
$ pinax tools
```

#### `pinax start <starter_project> <my_project> [--dev] [--location <path>]`

Create a new project based on a specific Pinax starter project.

`<starter_project>` must be one of the project names shown by `pinax projects`.

The `--dev` flag tells pinax-cli to install the latest starter project code from the repository rather than the most recent release.
Use this option if you require the latest version of a starter project.

The `--location <path>` flag tells pinax-cli where to create the new project. By default
the project is created in a sub-directory named `my_project`. 

## Change Log

### 1.1.3

* Drop support for Python 2.7 and Django < 2.0; require Python 3.4+ and Django 2.0+

### 1.1.2

* Use Django v1.11 for project creation if installed Python == 2.7
* Add usage examples, color, and sub-command short description to help
* Add `crayons` and `django` requirements to setup.py

### 1.1.1

* Fix post-start cleanup path references

### 1.1.0

* Drop Python 3.3 support
* Standardize documentation layout
* Move documentation into README.md
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description
* Improve .gitignore

### 1.0.0

* Add "apps", "demos", "themes", and "tools" commands.


## Contribute

For an overview on how contributing to Pinax works read this [blog post](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/)
and watch the included video, or read our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section.
For concrete contribution ideas, please see our
[Ways to Contribute/What We Need Help With](http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our [Pinax Slack team](http://slack.pinaxproject.com)
and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course
also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our blog post on [Open Source and Self-Care](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project
has a [code of conduct](http://pinaxproject.com/pinax/code_of_conduct/).
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject)
and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-2018 James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
