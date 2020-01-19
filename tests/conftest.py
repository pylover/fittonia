import functools

import pytest
import bddrest
from yhttp.extensions.pony.testing import freshdb


@pytest.fixture
def app():
    from fittonia import app
    return app


@pytest.fixture
def story(app):
    return functools.partial(bddrest.Given, app)

