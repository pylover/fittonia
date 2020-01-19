from bddrest import when, status, response
from pony.orm import db_session as dbsession

from fittonia import Resource


def test_globalcontent_get(app, story):
    @dbsession
    def mockup():
        Resource(path='', content=dict(foo='bar'))
        Resource(path='bar', content=dict(bar='baz'))

    app.ready()
    mockup()

    with story('Get a global content by anonymous user'):
        assert status == 200
        assert response.json == {'foo': 'bar'}

        when('Get with trailing slash', '/bar/')
        assert status == 200
        assert response.json == {'bar': 'baz'}

        when('Get 404!', '/neverland')
        assert status == 404


def test_globalcontent_post(app, story):
    app.ready()
    token = app.jwt.dump(dict(name='oscar', roles=['admin'])).decode()

    with story(
        'Create a global content by admin',
        '/',
        'POST',
        json=dict(foo='bar'),
        headers=[f'Authorization: {token}']
    ):
        assert status == 200
        assert response.json == {'foo': 'bar'}

        when(None, verb='GET')
        assert status == 200
        assert response.json == {'foo': 'bar'}


def test_globalcontent_update(app, story):
    @dbsession
    def mockup():
        Resource(path='', content=dict(foo='bar'))

    app.ready()
    token = app.jwt.dump(dict(name='oscar', roles=['admin'])).decode()
    mockup()

    with story(
        'Update a global content',
        '/',
        'UPDATE',
        json=dict(foo='baz'),
        headers=[f'Authorization: {token}'],
    ):
        assert status == 200
        assert response.json == {'foo': 'baz'}

        when(None, verb='GET')
        assert status == 200
        assert response.json == {'foo': 'baz'}

        when('Update an invalid item', '/neverland')
        assert status == 404


def test_globalcontent_delete(app, story):
    @dbsession
    def mockup():
        Resource(path='', content=dict(foo='bar'))

    app.ready()
    token = app.jwt.dump(dict(name='oscar', roles=['admin'])).decode()
    mockup()

    with story(
        'Delete a global content',
        '/',
        'DELETE',
        headers=[f'Authorization: {token}']
    ):
        assert status == 200
        assert response.json == {'foo': 'bar'}

        when('Get the deleted resource', verb='GET')
        assert status == 404

        when('Delete an invalid item', '/neverland')
        assert status == 404



