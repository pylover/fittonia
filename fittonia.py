import os
import sys

from yhttp import Application, json, statuses
from pony.orm import Required, PrimaryKey, Json, db_session as dbsession, \
    Optional
from yhttp.extensions import pony as ponyext, auth as authext


__version__ = '0.1.0'


app = Application()
authenticate = authext.install(app)
db = ponyext.install(app)
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/fittonia

jwt:
  secret: foobarbaz
''')


class Resource(db.Entity):
    id = PrimaryKey(int, auto=True)
    path = Required(str, unique=True)
    author = Optional(str)
    content = Required(Json)


@app.route(r'/users/(.*)(/.*)?')
@dbsession
@json
def get(req, username, path=None):
    path = f'/users/{username}{path or ""}'
    if path.endswith('/'):
        path = path[:-1]

    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    return resource.content


@app.route(r'/users/(.*)(/.*)?')
@authenticate()
@dbsession
@json
def post(req, username, path=None):
    if req.identity.name != username:
        raise statuses.forbidden()

    path = f'/users/{username}{path or ""}'
    r = Resource(path=path, author=username, content=req.form)
    return req.form


@app.route(r'/users/(.*)')
@authenticate()
@dbsession
@json
def delete(req, path=None):
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    resource.delete()
    return resource.content


@app.route(r'/users/(.*)')
@authenticate()
@dbsession
@json
def update(req, path=None):
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    resource.content = req.form
    return req.form



if 'SERVER_SOFTWARE' in os.environ:
    app.ready()

