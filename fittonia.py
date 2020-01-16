import yhttp
from pony.orm import Required, PrimaryKey, Json
from yhttp.extensions.pony import setup as setuporm, dbsession, \
    configure as configureorm


__version__ = '0.1.0'


app = yhttp.Application()
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/fittonia
''')


db = setuporm(app)


def configure(filename=None):
    if filename:
        app.settings.loadfile(filename)

    configureorm(app)


class Resource(db.Entity):
    id = PrimaryKey(int, auto=True)
    path = Required(str, unique=True)
    content = Required(Json)


@app.route(r'/(.*)')
@dbsession
def get(req, path=None):
    query = Resource.select(lambda r: r.path == path)
    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    return b'Hello'


