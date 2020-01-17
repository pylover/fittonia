import os

import yhttp
from pony.orm import Required, PrimaryKey, Json, db_session as dbsession
from yhttp.extensions import pony as ponyext


__version__ = '0.1.0'


app = yhttp.Application()
app.extend(ponyext)
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/fittonia
''')


class Resource(app.db.Entity):
    id = PrimaryKey(int, auto=True)
    path = Required(str, unique=True)
    content = Required(Json)


@app.route(r'/(.*)')
@dbsession
def get(req, path=None):
    query = Resource.select(lambda r: r.path == path)
    return b'Hello'


if 'SERVER_SOFTWARE' in os.environ:
    app.configure_extensions()

