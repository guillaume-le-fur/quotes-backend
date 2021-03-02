import os
import tempfile

import pytest

from app import app, create_tables
from db import db


@pytest.fixture
def client():
    """
    Mock client to use during testing
    """

    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
