import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
  
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  
        "SECRET_KEY": "testsecret"
    })

    with app.app_context():
        db.create_all()  
        user = User(username="testuser")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    yield app 

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()  

@pytest.fixture
def runner(app):
    return app.test_cli_runner()  

def test_homepage_redirect(client):
    
    response = client.get('/')
    assert response.status_code == 302  # nosec B101
    assert "/login" in response.headers["Location"]  # nosec B101

def test_user_created(app):
    
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        assert user is not None  # nosec B101

        assert user.check_password("password123")  # nosec B101

def test_login(client):
    
    response = client.post('/login', data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200  # nosec B101
    assert b"Logout" in response.data   # nosec B101
