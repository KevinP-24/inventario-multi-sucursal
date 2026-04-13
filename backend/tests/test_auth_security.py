def test_login_jwt_retorna_token_y_usuario(client):
    respuesta = client.post(
        "/api/v1/auth/login",
        json={
            "correo": "admin.general@multisucursal.local",
            "password": "Admin123*",
        },
    )

    datos = respuesta.get_json()
    assert respuesta.status_code == 200
    assert datos["token_type"] == "Bearer"
    assert datos["access_token"]
    assert datos["usuario"]["rol"]["nombre"] == "Admin general"


def test_endpoint_privado_sin_token_responde_401(client):
    respuesta = client.get("/api/v1/productos/listar_productos")

    assert respuesta.status_code == 401


def test_admin_puede_consultar_productos(client, auth_headers):
    respuesta = client.get("/api/v1/productos/listar_productos", headers=auth_headers)

    assert respuesta.status_code == 200
    assert "data" in respuesta.get_json()


def test_operario_no_puede_administrar_usuarios(client, operario_token):
    respuesta = client.get(
        "/api/v1/usuarios/listar_usuarios",
        headers={"Authorization": f"Bearer {operario_token}"},
    )

    assert respuesta.status_code == 403
