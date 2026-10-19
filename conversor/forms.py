from django import forms

BASES = (
    ("2", "Binario (2)"),
    ("8", "Octal (8)"),
    ("10", "Decimal (10)"),
    ("16", "Hexadecimal (16)"),
)
DIGITOS_POR_BASE = {
    "2": set("01"),
    "8": set("01234567"),
    "10": set("0123456789"),
    "16": set("0123456789abcdefABCDEF"),
}
VALOR_MINIMO = 0
VALOR_MAXIMO = 65535


class ConversionForm(forms.Form):

    numero = forms.CharField(
        label="Número",
        max_length=50,
        strip=True,
        required=True,
        error_messages={
            "required": "No se ingresó ningún número.",
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. 1010, 17, 255 o FF",
                "autocomplete": "off",
            }
        ),
    )
    base_origen = forms.ChoiceField(
        label="Base de origen",
        choices=BASES,
        required=True,
        error_messages={
            "required": "Debe seleccionar una base de origen.",
        },
    )

    def clean_numero(self):
        numero = self.cleaned_data.get("numero", "")
        if numero == "" or numero is None:
            raise forms.ValidationError("No se ingresó ningún número.")
        if numero.startswith("-"):
            raise forms.ValidationError("No se permiten valores negativos.")
        return numero

    def clean(self):
        cleaned = super().clean()
        numero = cleaned.get("numero")
        base = cleaned.get("base_origen")

        if not numero or not base:
            return cleaned

        digitos_validos = DIGITOS_POR_BASE[base]
        invalidos = sorted({c for c in numero if c not in digitos_validos})
        if invalidos:
            raise forms.ValidationError(
                "Dígitos inválidos para la base {}: {}".format(
                    base, ", ".join(invalidos)
                )
            )

        try:
            decimal = int(numero, int(base))
        except ValueError:
            raise forms.ValidationError("No se pudo convertir el número.")

        if decimal < VALOR_MINIMO or decimal > VALOR_MAXIMO:
            raise forms.ValidationError(
                "El valor debe estar entre 0 y 65 535 (se ingresó {}).".format(
                    decimal
                )
            )

        cleaned["decimal"] = decimal
        return cleaned


class TextoForm(forms.Form):

    texto = forms.CharField(
        label="Texto",
        max_length=20,
        required=True,
        error_messages={
            "required": "No se ingresó ningún texto.",
            "max_length": "El texto no debe superar los 20 caracteres.",
        },
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Escribe aquí el texto",
                "maxlength": "20",
            }
        ),
    )

    def clean_texto(self):
        texto = self.cleaned_data.get("texto", "")
        if texto is None or texto.strip() == "":
            raise forms.ValidationError("No se ingresó ningún texto.")
        return texto
