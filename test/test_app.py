import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    # Buat instance Flask app untuk testing
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  # Nonaktifkan CSRF untuk testing form
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # DB sementara di RAM
        "SECRET_KEY": "testsecret"
    })

    with app.app_context():
        db.create_all()  # buat tabel
        # Tambah user test dengan set_password
        user = User(username="testuser")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    yield app  # beri app ke test yang membutuhkan

    # Cleanup setelah test selesai
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()  # client untuk request ke app

@pytest.fixture
def runner(app):
    return app.test_cli_runner()  # untuk testing CLI command jika ada

def test_homepage_redirect(client):
    # Cek homepage redirect (misal ke /login)
    response = client.get('/')
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_user_created(app):
    # Cek user testuser ada di database
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        assert user is not None
        # Cek password benar dengan metode verify_password (asumsi ada)
        assert user.check_password("password123")

def test_login(client):
    # Tes login dengan user testuser (asumsi route /login POST)
    response = client.post('/login', data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Logout" in response.data  # Contoh cek ada tombol Logout di halaman setelah login
