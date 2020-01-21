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

##### Bash Autocompletion

```bash
fittonia completion install
```

Deactivate and activate your virtual environment to use bash auto completion.

```bash
deactivate && workon <virtualenv>
```

##### Help?

Use the `-h/--help` to discover all command line features.

```bash
fittonia --help
fittonia db --help
fittonia jwt --help
```

##### Create database

```bash
fittonia db create [-p [postgres-password]]  # default is: postgres
```

### Web API

You can use any `wsgi` server to serve fittonia, such as `gunicorn`:
create a file named:

wsgi.py
```python
from fittonia import app
```

Then

```bash
gunicorn wsgi:app
```

Or you may use the `serve` command to run the python's builtin wsgi server:

```bash
fittonia serve [-b 8080]
```

### WebAPI Usage

First, obtain a token via `fittonia jwt create <payload>` to use web service.

```bash
T=$(fittonia jwt create '{"roles": ["admin"], "name": "yourname"}')
echo $T
```

Then issue a `curl` to create a json resource for example: `/foo':

```bash
curl \
    -H"Authorization: $T" \
    -H"Content-Type: application/json" \
    -X POST \
    -d'{"page": "foo"}' \
    http://localhost:8080/foo
```

##### GET

Get the `/foo` by:

```bash
curl localhost:8080/foo
```

There are some extra verbs to manage the web resources you already saved:

##### UPDATE

```bash
curl \
    -H"Authorization: $T" \
    -H"Content-Type: application/json" \
    -X UPDATE \
    -d'{"page": "foo", "bar": "baz"}' \
    http://localhost:8080/foo
```

##### DELETE

```bash
curl \
    -H"Authorization: $T" \
    -X DELETE \
    http://localhost:8080/foo
```

