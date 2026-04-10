TIPOS_DOCUMENTO_BASE = [
    {
        "codigo": "CC",
        "nombre": "Cedula de ciudadania",
        "descripcion": "Documento de identificacion para ciudadanos colombianos mayores de edad.",
    },
    {
        "codigo": "TI",
        "nombre": "Tarjeta de identidad",
        "descripcion": "Documento de identificacion para menores de edad en Colombia.",
    },
    {
        "codigo": "CE",
        "nombre": "Cedula de extranjeria",
        "descripcion": "Documento para extranjeros residentes en Colombia.",
    },
    {
        "codigo": "NIT",
        "nombre": "Numero de identificacion tributaria",
        "descripcion": "Identificacion tributaria de empresas o personas ante la DIAN.",
    },
    {
        "codigo": "PAS",
        "nombre": "Pasaporte",
        "descripcion": "Documento de viaje usado como identificacion.",
    },
    {
        "codigo": "PEP",
        "nombre": "Permiso especial de permanencia",
        "descripcion": "Documento usado por poblacion migrante segun disposiciones colombianas.",
    },
    {
        "codigo": "PPT",
        "nombre": "Permiso por proteccion temporal",
        "descripcion": "Documento de identificacion para poblacion migrante venezolana en Colombia.",
    },
]


def convertir_tipo_documento_a_respuesta(tipo_documento):
    """Convierte un tipo de documento SQLAlchemy a diccionario."""
    return tipo_documento.convertir_a_diccionario()
