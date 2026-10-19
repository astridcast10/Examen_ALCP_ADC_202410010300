from django.shortcuts import render

from .forms import ConversionForm, TextoForm


BITS_POR_BYTE = 8


def analizar_numero(valor, base):
    errores = []

    if not valor or not valor.strip():
        errores.append("No se ingresó ningún número.")
        return errores, None

    valor = valor.strip()

    if valor.startswith("-"):
        errores.append("No se permiten valores negativos.")
        return errores, None

    digitos_validos = {
        "2": set("01"),
        "8": set("01234567"),
        "10": set("0123456789"),
        "16": set("0123456789abcdefABCDEF"),
    }[str(base)]

    invalidos = [c for c in valor if c not in digitos_validos]
    if invalidos:
        errores.append(
            "Dígitos inválidos para la base {}: {}".format(
                base, ", ".join(sorted(set(invalidos)))
            )
        )
        return errores, None

    try:
        decimal = int(valor, base)
    except ValueError:
        errores.append("No se pudo convertir el número.")
        return errores, None

    if decimal < 0 or decimal > 65535:
        errores.append(
            "El valor debe estar entre 0 y 65 535 (se ingresó {}).".format(decimal)
        )
        return errores, None

    bits_significativos = max(1, decimal.bit_length())
    bytes_necesarios = (bits_significativos + BITS_POR_BYTE - 1) // BITS_POR_BYTE
    bits_ajustados = bytes_necesarios * BITS_POR_BYTE

    binario = format(decimal, "b").zfill(bits_ajustados)
    octal = format(decimal, "o")
    hexadecimal = format(decimal, "X")

    resultado = {
        "valor_original": valor,
        "base_origen": base,
        "decimal": decimal,
        "binario": binario,
        "octal": octal,
        "hexadecimal": hexadecimal,
        "bits_significativos": bits_significativos,
        "bytes": bytes_necesarios,
    }
    return errores, resultado


def analizar_texto(texto):
    caracteres = []
    for caracter in texto:
        codigo = ord(caracter)
        bytes_utf8 = caracter.encode("utf-8")
        caracteres.append(
            {
                "caracter": caracter,
                "decimal": codigo,
                "punto_codigo": "U+{:04X}".format(codigo),
                "hexadecimal": "{:X}".format(codigo),
                "bytes_utf8": " ".join("{:02X}".format(b) for b in bytes_utf8),
            }
        )
    return caracteres


def index(request):
    conversion_form = ConversionForm()
    texto_form = TextoForm()

    conversion_resultado = None
    conversion_errores = []
    texto_caracteres = None
    texto_errores = []

    if request.method == "POST":
        if "convertir" in request.POST:
            conversion_form = ConversionForm(request.POST)
            if conversion_form.is_valid():
                conversion_errores, conversion_resultado = analizar_numero(
                    conversion_form.cleaned_data["numero"],
                    int(conversion_form.cleaned_data["base_origen"]),
                )
            else:
                conversion_errores = _errores_formulario(conversion_form)
        elif "analizar_texto" in request.POST:
            texto_form = TextoForm(request.POST)
            if texto_form.is_valid():
                texto_caracteres = analizar_texto(texto_form.cleaned_data["texto"])
            else:
                texto_errores = _errores_formulario(texto_form)

    return render(
        request,
        "conversor/index.html",
        {
            "conversion_form": conversion_form,
            "texto_form": texto_form,
            "conversion_resultado": conversion_resultado,
            "conversion_errores": conversion_errores,
            "texto_caracteres": texto_caracteres,
            "texto_errores": texto_errores,
        },
    )


def _errores_formulario(form):
    mensajes = []
    for campo, errores in form.errors.items():
        etiqueta = form[campo].label if campo != "__all__" else ""
        for error in errores:
            if etiqueta:
                mensajes.append("{}: {}".format(etiqueta, error))
            else:
                mensajes.append(error)
    return mensajes
