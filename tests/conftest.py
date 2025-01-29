import pytest
from flaskr import create_app, db
from flaskr.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # In-memory database for testing
        'SECRET_KEY': 'test_secret_key'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()  # Cleanup after tests

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def new_user(app):
    with app.app_context():
        user = User(
            email="testuser@example.com",
            password=generate_password_hash("TestPass123!", method='pbkdf2:sha256', salt_length=16),
            first_name="TestUser"
        )
        db.session.add(user)
        db.session.commit()
        return user
