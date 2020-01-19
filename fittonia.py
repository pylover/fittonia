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



usersroute = app.route(r'/users/([a-zA-Z0-9_]+)(/.*)?')
globalroute = app.route(r'/(.*)?')


class Resource(db.Entity):
    id = PrimaryKey(int, auto=True)
    path = Required(str, unique=True)
    author = Optional(str)
    content = Required(Json)


def ensurepath(req, username, path):
    if req.identity.name != username:
        raise statuses.forbidden()

    return f'/users/{username}{path or ""}'


@usersroute
@authenticate()
@dbsession
@json
def post(req, username, path=None):
    path = ensurepath(req, username, path)
    Resource(path=path, author=username, content=req.form)
    return req.form


@usersroute
@authenticate()
@dbsession
@json
def delete(req, username, path=None):
    path = ensurepath(req, username, path)
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    resource.delete()
    return resource.content


@usersroute
@authenticate()
@dbsession
@json
def update(req, username, path=None):
    path = ensurepath(req, username, path)
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    resource.content = req.form
    return req.form


@globalroute
@dbsession
@json
def get(req, path=None):
    if path.endswith('/'):
        path = path[:-1]

    path = f'/{path}'
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    return resource.content


if 'SERVER_SOFTWARE' in os.environ:  # pragma: no cover
    app.ready()

