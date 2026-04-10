def test_venta_sin_stock_no_se_confirma(client, auth_headers):
    respuesta = client.post(
        "/api/v1/ventas/crear_venta",
        headers=auth_headers,
        json={
            "id_sucursal": 1,
            "id_usuario": 1,
            "id_lista_precio": 1,
            "detalles": [
                {
                    "id_producto": 1,
                    "id_producto_unidad": 1,
                    "cantidad": 999999,
                    "descuento": 0,
                }
            ],
        },
    )

    datos = respuesta.get_json()
    assert respuesta.status_code == 400
    assert any("stock" in clave for clave in datos["errors"])


def test_alertas_stock_bajo_responde_con_token(client, auth_headers):
    respuesta = client.get(
        "/api/v1/inventario-sucursal/listar_alertas_stock_bajo",
        headers=auth_headers,
    )

    assert respuesta.status_code == 200
    assert "data" in respuesta.get_json()


def test_dashboard_principales_responden(client, auth_headers):
    endpoints = [
        "/api/v1/dashboard/volumen_ventas",
        "/api/v1/dashboard/rotacion_demanda",
        "/api/v1/dashboard/transferencias_activas",
        "/api/v1/dashboard/reabastecimiento",
        "/api/v1/dashboard/rendimiento_sucursales",
    ]

    for endpoint in endpoints:
        respuesta = client.get(endpoint, headers=auth_headers)
        assert respuesta.status_code == 200
        assert "data" in respuesta.get_json()
