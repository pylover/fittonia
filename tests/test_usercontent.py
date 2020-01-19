from bddrest import when, status, response
from pony.orm import db_session as dbsession

from fittonia import Resource


def test_usercontent_get(app, story):
    @dbsession
    def mockup():
        Resource(path='/users/oscar', author='oscar', content=dict(foo='bar'))
        Resource(path='/users/oscar/bar', author='oscar',
                 content=dict(bar='baz'))

    app.ready()
    mockup()

    with story('Get a user content by anonymous user', '/users/oscar'):
        assert status == 200
        assert response.json == {'foo': 'bar'}

        when('Get with trailing slash', '/users/oscar/')
        assert status == 200
        assert response.json == {'foo': 'bar'}

        when('Get another user content', '/users/oscar/bar')
        assert status == 200
        assert response.json == {'bar': 'baz'}

        when('Get 404!', '/users/oscar/neverland')
        assert status == 404

        when('Try to update a user content by anonymous', verb='POST', form={
            'foo': 'baz'
        })
        assert status == 401


def test_usercontent_post(app, story):
    app.ready()
    token = app.jwt.dump(dict(name='oscar')).decode()

    with story(
        'Create a user content by loged-in user',
        '/users/oscar',
        'POST',
        json=dict(foo='bar'),
        headers=[f'Authorization: {token}']
    ):
        assert status == 200
        assert response.json == {'foo': 'bar'}

        when('Try to post another user\'s content', '/users/pascal')
        assert status == 403

