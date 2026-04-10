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
    click.echo(f"Conversiones producto-unidad listas: {len(resultado['producto_unidades'])}")
    click.echo(f"Inventario por sucursal listo: {len(resultado['inventario_sucursal'])}")
    click.echo(f"Proveedores listos: {len(resultado['proveedores'])}")
    click.echo(f"Listas de precio listas: {len(resultado['listas_precio'])}")
    click.echo(f"Precios por producto listos: {len(resultado['precios_producto'])}")
    click.echo(f"Transportistas listos: {len(resultado['transportistas'])}")
    click.echo(f"Rutas logisticas listas: {len(resultado['rutas_logistica'])}")
    click.echo(f"Parametros del sistema listos: {len(resultado['parametros_sistema'])}")
