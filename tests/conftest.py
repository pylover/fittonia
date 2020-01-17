import pytest

import fittonia


@pytest.fixture
def app():
    dbname = 'fittonia_test'
    fittonia.app.settings.merge(f'''
    db:
      url: postgres://postgres:postgres@localhost/{dbname}
    ''')



