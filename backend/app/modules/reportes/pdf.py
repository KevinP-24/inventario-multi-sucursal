from datetime import datetime


def generar_pdf_tabular(titulo, subtitulo, columnas, filas):
    """Genera un PDF tabular sencillo usando solo libreria estandar."""
    paginas = construir_paginas(titulo, subtitulo, columnas, filas)
    objetos = []

    objetos.append("<< /Type /Catalog /Pages 2 0 R >>")
    objetos.append(None)
    objetos.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objetos.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    contenido_ids = []
    pagina_ids = []
    for pagina in paginas:
        contenido = construir_stream_pagina(pagina)
        contenido_ids.append(len(objetos) + 1)
        objetos.append(f"<< /Length {len(contenido.encode('latin-1'))} >>\nstream\n{contenido}\nendstream")

        pagina_ids.append(len(objetos) + 1)
        objetos.append(
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Contents {contenido_ids[-1]} 0 R /Resources "
            "<< /Font << /F1 3 0 R /F2 4 0 R >> >> >>"
        )

    kids = " ".join(f"{pagina_id} 0 R" for pagina_id in pagina_ids)
    objetos[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(pagina_ids)} >>"

    return construir_documento_pdf(objetos)


def construir_paginas(titulo, subtitulo, columnas, filas):
    """Parte filas en paginas con cabecera repetida."""
    filas_por_pagina = 28
    filas = filas or [["Sin datos para los filtros seleccionados."]]
    paginas = []

    for indice in range(0, len(filas), filas_por_pagina):
        paginas.append({
            "titulo": titulo,
            "subtitulo": subtitulo,
            "columnas": columnas,
            "filas": filas[indice: indice + filas_por_pagina],
            "pagina": len(paginas) + 1,
        })

    return paginas


def construir_stream_pagina(pagina):
    """Construye comandos PDF para una pagina."""
    comandos = [
        "BT",
        "/F2 16 Tf",
        "50 750 Td",
        f"({escapar_texto_pdf(pagina['titulo'])}) Tj",
        "/F1 9 Tf",
        "0 -18 Td",
        f"({escapar_texto_pdf(pagina['subtitulo'])}) Tj",
        "0 -18 Td",
        f"(Generado: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC) Tj",
        "ET",
    ]

    y = 690
    x_inicial = 50
    ancho_columna = 512 / max(len(pagina["columnas"]), 1)

    comandos.extend(["BT", "/F2 8 Tf"])
    for indice, columna in enumerate(pagina["columnas"]):
        comandos.append(f"1 0 0 1 {x_inicial + indice * ancho_columna:.2f} {y} Tm")
        comandos.append(f"({escapar_texto_pdf(columna)}) Tj")
    comandos.append("ET")

    y -= 18
    comandos.extend(["BT", "/F1 7 Tf"])
    for fila in pagina["filas"]:
        for indice, valor in enumerate(fila):
            x = x_inicial + indice * ancho_columna
            texto = recortar_texto(str(valor), int(ancho_columna / 4.2))
            comandos.append(f"1 0 0 1 {x:.2f} {y} Tm")
            comandos.append(f"({escapar_texto_pdf(texto)}) Tj")
        y -= 18
    comandos.append("ET")

    comandos.extend([
        "BT",
        "/F1 8 Tf",
        "50 35 Td",
        f"(Pagina {pagina['pagina']}) Tj",
        "ET",
    ])

    return "\n".join(comandos)


def construir_documento_pdf(objetos):
    """Ensambla objetos, referencias y trailer del PDF."""
    partes = ["%PDF-1.4\n"]
    offsets = [0]

    for indice, objeto in enumerate(objetos, start=1):
        offsets.append(sum(len(parte.encode("latin-1")) for parte in partes))
        partes.append(f"{indice} 0 obj\n{objeto}\nendobj\n")

    inicio_xref = sum(len(parte.encode("latin-1")) for parte in partes)
    partes.append(f"xref\n0 {len(objetos) + 1}\n")
    partes.append("0000000000 65535 f \n")
    for offset in offsets[1:]:
        partes.append(f"{offset:010d} 00000 n \n")

    partes.append(
        "trailer\n"
        f"<< /Size {len(objetos) + 1} /Root 1 0 R >>\n"
        "startxref\n"
        f"{inicio_xref}\n"
        "%%EOF"
    )

    return "".join(partes).encode("latin-1", errors="replace")


def escapar_texto_pdf(texto):
    """Escapa caracteres especiales para strings PDF."""
    return (
        texto.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .encode("latin-1", errors="replace")
        .decode("latin-1")
    )


def recortar_texto(texto, longitud):
    """Evita que las celdas se monten sobre la siguiente columna."""
    if len(texto) <= longitud:
        return texto

    return f"{texto[:max(longitud - 3, 1)]}..."
