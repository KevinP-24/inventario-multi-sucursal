from werkzeug.security import check_password_hash, generate_password_hash


def generar_hash_password(password_plano):
    """Convierte una clave normal en un hash seguro para guardarlo en la BD.

    Guardamos el hash y no la clave original. Asi, si alguien mira la base
    de datos, no puede ver las contrasenas reales de los usuarios.
    """
    return generate_password_hash(password_plano)


def verificar_password(password_plano, password_hash):
    """Compara la clave escrita por el usuario contra el hash guardado."""
    return check_password_hash(password_hash, password_plano)
