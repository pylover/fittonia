import os
import sys

import yhttp
from pony.orm import Required, PrimaryKey, Json, db_session as dbsession
from yhttp.extensions import pony as ponyext


__version__ = '0.1.0'


app = yhttp.Application()
db = ponyext.install(app)
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/fittonia
''')


class Resource(db.Entity):
    id = PrimaryKey(int, auto=True)
    path = Required(str, unique=True)
    content = Required(Json)


@app.route(r'/(.*)')
@dbsession
@yhttp.json
def get(req, path=None):
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise yhttp.statuses.notfound()

    return resource.content


@app.route(r'/(.*)')
@dbsession
@yhttp.json
def delete(req, path=None):
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise yhttp.statuses.notfound()

    resource.delete()
    return resource.content


@app.route(r'/(.*)')
@dbsession
@yhttp.json
def update(req, path=None):
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise yhttp.statuses.notfound()

    resource.content = req.form
    return req.form


@app.route(r'/(.*)')
@dbsession
@yhttp.json
def post(req, path=None):
    r = Resource(path=path, content= req.form)
    return req.form


if 'SERVER_SOFTWARE' in os.environ:
    app.ready()

