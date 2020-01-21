# fittonia

[![Build Status](https://travis-ci.org/pylover/fittonia.svg?branch=master)](https://travis-ci.org/pylover/fittonia)
[![Coverage Status](https://coveralls.io/repos/github/pylover/fittonia/badge.svg?branch=master)](https://coveralls.io/github/pylover/fittonia?branch=master)


Store, Update and get JSON document using URL.


### Install

It's highly recommended to use virtualenv to install the fittonia. my favorite
virtualenv toolbox is [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/).

So, the `workon` command on this page is related to the `virtualenvwrapper`
package and you may use your favorite virtualenv utility such as python's
builtin.

First install required system packages:

```bash
sudo apt install libpq-dev postgresql python3-dev
```

Then install the fittonia:

```bash
git clone https://github.com/pylover/fittonia.git
cd fittonia
pip install [-e] .
```

Or

```bash
pip install git+https://github.com/pylover/fittonia.git
```


### Usage

#### CLI

#### Bash Autocompletion

```bash
fittonia completion install
```


#### Help?

Use the `-h/--help` to discover all command line features.

```bash
fittonia --help
fittonia db --help
fittonia jwt --help
```


Deactivate and activate your virtual environment to use bash auto completion.

```bash
deactivate && workon <virtualenv>
```

#### Create database

```bash
fittonia db create [-p [postgres-password]]
```


