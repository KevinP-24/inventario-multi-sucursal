def test_health_es_publico(client):
    respuesta = client.get("/api/v1/health/")

    assert respuesta.status_code == 200
    assert respuesta.get_json()["message"] == "API multi-sucursal operativa"
