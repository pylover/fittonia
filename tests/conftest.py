import functools

import pytest
import bddrest
from yhttp.extensions.pony import createdbmanager


@pytest.fixture
def app():
    from fittonia import app

    host='localhost'
    user='postgres'
    password='postgres'
    dbname = 'yhttpponytestdb'

    dbmanager = createdbmanager(host, 'postgres', user, password)
    dbmanager.create(dbname, dropifexists=True)
    freshurl = f'postgres://{user}:{password}@{host}/{dbname}'
    app.settings.merge(f'''
    db:
      url: {freshurl}
    ''')
    yield app
    app.shutdown()
    dbmanager.dropifexists(dbname)


@pytest.fixture
def story(app):
    return functools.partial(bddrest.Given, app)

