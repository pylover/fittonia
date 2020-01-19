from bddrest import when, status, response
from pony.orm import db_session as dbsession

from fittonia import Resource


def test_usercontent(app, story, freshdb):
    app.settings.merge(f'''
    db:
      url: {freshdb}
    ''')

    @dbsession
    def mockup():
        Resource(path='/users/foo', author='foo', content=dict(foo='bar'))

    app.ready()
    mockup()

    with story('Get a user content by anonymous user', '/users/foo'):
        print(response.text)
        assert status == 200
        assert response.json == {'foo': 'bar'}

        when('Try to update a user content by anonymous', verb='POST', form={
            'foo': 'baz'
        })
        assert status == 401

