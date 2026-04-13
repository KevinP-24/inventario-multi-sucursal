def test_reportes_pdf_responden_archivo_pdf(client, auth_headers):
    endpoints = [
        "/api/v1/reportes/ventas/pdf?fecha_desde=2026-01-01&id_sucursal=1",
        "/api/v1/reportes/inventario/pdf?fecha_desde=2026-01-01&id_sucursal=1",
        "/api/v1/reportes/transferencias/pdf?fecha_desde=2026-01-01&id_sucursal=1",
    ]

    for endpoint in endpoints:
        respuesta = client.get(endpoint, headers=auth_headers)

        assert respuesta.status_code == 200
        assert respuesta.content_type == "application/pdf"
        assert respuesta.data.startswith(b"%PDF")
