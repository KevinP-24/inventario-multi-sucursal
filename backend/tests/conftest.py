import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, correo, password):
    respuesta = client.post(
        "/api/v1/auth/login",
        json={"correo": correo, "password": password},
    )
    assert respuesta.status_code == 200
    return respuesta.get_json()["access_token"]


@pytest.fixture()
def admin_token(client):
    return login(client, "admin.general@multisucursal.local", "Admin123*")


@pytest.fixture()
def operario_token(client):
    return login(client, "operario.inventario@multisucursal.local", "Inventario123*")


@pytest.fixture()
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
