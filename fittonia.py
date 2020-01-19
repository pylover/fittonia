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
everyone = authenticate()
admin = authenticate(roles='admin')


class Resource(db.Entity):
    id = PrimaryKey(int, auto=True)
    path = Optional(str, unique=True)
    author = Optional(str, nullable=True)
    content = Required(Json)


def ensureglobalpath(req, path):
    path = path or ''
    if path.endswith('/'):
        path = path[:-1]

    return path


def ensurepath(req, username, path):
    if req.identity.name != username:
        raise statuses.forbidden()

    return f'users/{username}{path or ""}'


def getglobalresource(req, path):
    path = ensureglobalpath(req, path)
    query = Resource.select(lambda r: r.path == path and r.author is None)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    return resource

def getuserresource(req, username, path):
    path = ensurepath(req, username, path)
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    return resource


@usersroute
@everyone
@dbsession
@json
def post(req, username, path=None):
    path = ensurepath(req, username, path)
    Resource(path=path, author=username, content=req.form)
    return req.form


@usersroute
@everyone
@dbsession
@json
def delete(req, username, path=None):
    resource = getuserresource(req, username, path)
    resource.delete()
    return resource.content


@usersroute
@everyone
@dbsession
@json
def update(req, username, path=None):
    resource = getuserresource(req, username, path)
    resource.content = req.form
    return req.form


@globalroute
@dbsession
@json
def get(req, path=None):
    path = ensureglobalpath(req, path)
    query = Resource.select(lambda r: r.path == path)
    resource = query.first()
    if resource is None:
        raise statuses.notfound()

    return resource.content


@globalroute
@admin
@dbsession
@json
def post(req, path=None):
    path = ensureglobalpath(req, path)
    Resource(path=path, content=req.form)
    return req.form


@globalroute
@admin
@dbsession
@json
def update(req, path=None):
    resource = getglobalresource(req, path)
    resource.content = req.form
    return req.form


@globalroute
@admin
@dbsession
@json
def delete(req, path=None):
    resource = getglobalresource(req, path)
    resource.delete()
    return resource.content


if 'SERVER_SOFTWARE' in os.environ:  # pragma: no cover
    app.ready()

