import functools
import getpass

import psycopg2
import yhttp
from easycli import SubCommand, Argument
from pony.orm import Database, Required, PrimaryKey, Json, \
    set_sql_debug, db_session as dbsession


__version__ = '0.1.0'


db = Database()
app = yhttp.Application()
app.settings.merge('''
db:
  provider: postgres
  host: localhost
  user: postgres
  password: postgres
  database: fittonia
''')


def createrawdbconn(host, dbname, user, password):
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

@dbsession
def createdb(conn):
    dbname = app.settings.db.database
    dbuser = app.settings.db.user
    cursor = conn.cursor()
    try:
        r = cursor.execute(f'CREATE DATABASE {dbname} WITH OWNER {dbuser}')
    finally:
        cursor.close()


getdbpass = functools.partial(getpass.getpass, 'Enter db password: ')


class CreateDatabase(SubCommand):
    __command__ = 'create'
    __aliases__ = ['c']
    __arguments__ = [
        Argument('-H', '--host', default='localhost', help='DB hostname'),
        Argument('-d', '--database', default='postgres', help='DB name'),
        Argument('-u', '--user', default='postgres', help='DB username'),
        Argument(
            '-p', '--password',
            nargs='?',
            default='postgres',
            help='DB password'
        ),
    ]

    def __call__(self, args):
        if args.password is None:
            args.password = getdbpass()

        conn = createrawdbconn(
            user=args.user,
            password=args.password,
            host=args.host,
            dbname=args.database
        )
        createdb(conn)


class DatabaseCLI(SubCommand):
    __command__ = 'database'
    __aliases__ = ['db']
    __arguments__ = [
        CreateDatabase,
    ]


app.__cliarguments__.append(DatabaseCLI)


class Resource(db.Entity):
    id = PrimaryKey(int, auto=True)
    path = Required(str, unique=True)
    content = Required(Json)


def configure():
    db.bind(**app.settings.db)
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)


@app.route(r'/(.*)')
@dbsession
def get(req, path=None):
    query = Resource.select(lambda r: r.path == path)
    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    return b'Hello'


