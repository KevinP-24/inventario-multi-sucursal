import click
from flask import Blueprint

from app.database.seeders.base_data import ejecutar_seed_datos_base

seed_cli = Blueprint("seed_cli", __name__, cli_group="seed")


@seed_cli.cli.command("datos-base")
def seed_datos_base_command():
    """Carga roles y usuarios demo sin duplicarlos."""
    resultado = ejecutar_seed_datos_base()

    click.echo("Datos base verificados correctamente.")
    click.echo(f"Roles listos: {len(resultado['roles'])}")
    click.echo(f"Sucursales listas: {len(resultado['sucursales'])}")
    click.echo(f"Usuarios listos: {len(resultado['usuarios'])}")
    click.echo(f"Unidades de medida listas: {len(resultado['unidades_medida'])}")
    click.echo(f"Productos listos: {len(resultado['productos'])}")
