from django.test import TestCase
from django.urls import reverse


class AnalizadorTests(TestCase):

    def post_conversion(self, numero, base):
        return self.client.post(
            reverse("conversor:index"),
            {"numero": numero, "base_origen": base, "convertir": "1"},
        )

    def post_texto(self, texto):
        return self.client.post(
            reverse("conversor:index"),
            {"texto": texto, "analizar_texto": "1"},
        )

    # --- Conversiones válidas ------------------------------------------------

    def test_conversion_binario_valida(self):
        respuesta = self.post_conversion("1111", "2")
        self.assertEqual(respuesta.status_code, 200)
        resultado = respuesta.context["conversion_resultado"]
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["decimal"], 15)
        self.assertEqual(resultado["binario"], "00001111")
        self.assertEqual(resultado["octal"], "17")
        self.assertEqual(resultado["hexadecimal"], "F")
        self.assertEqual(resultado["bits_significativos"], 4)
        self.assertEqual(resultado["bytes"], 1)

    def test_conversion_decimal_valida(self):
        respuesta = self.post_conversion("255", "10")
        resultado = respuesta.context["conversion_resultado"]
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["decimal"], 255)
        self.assertEqual(resultado["binario"], "11111111")
        self.assertEqual(resultado["octal"], "377")
        self.assertEqual(resultado["hexadecimal"], "FF")
        self.assertEqual(resultado["bits_significativos"], 8)
        self.assertEqual(resultado["bytes"], 1)

    def test_conversion_octal_valida(self):
        respuesta = self.post_conversion("17", "8")
        resultado = respuesta.context["conversion_resultado"]
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["decimal"], 15)

    def test_conversion_hexadecimal_valida(self):
        respuesta = self.post_conversion("ff", "16")
        resultado = respuesta.context["conversion_resultado"]
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["decimal"], 255)
        self.assertEqual(resultado["hexadecimal"], "FF")

    def test_limite_superior_rango_65535(self):
        respuesta = self.post_conversion("65535", "10")
        resultado = respuesta.context["conversion_resultado"]
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["decimal"], 65535)
        self.assertEqual(resultado["binario"], "1111111111111111")
        self.assertEqual(resultado["bits_significativos"], 16)
        self.assertEqual(resultado["bytes"], 2)

    def test_cero(self):
        respuesta = self.post_conversion("0", "10")
        resultado = respuesta.context["conversion_resultado"]
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["decimal"], 0)
        self.assertEqual(resultado["binario"], "00000000")
        self.assertEqual(resultado["bits_significativos"], 1)
        self.assertEqual(resultado["bytes"], 1)

    # --- Errores de base o rango ---------------------------------------------

    def test_digitos_invalidos_para_la_base(self):
        respuesta = self.post_conversion("12", "2")
        errores = respuesta.context["conversion_errores"]
        self.assertEqual(respuesta.context["conversion_resultado"], None)
        self.assertTrue(any("Dígitos inválidos" in e for e in errores))

    def test_letra_en_decimal(self):
        respuesta = self.post_conversion("1A", "10")
        errores = respuesta.context["conversion_errores"]
        self.assertEqual(respuesta.context["conversion_resultado"], None)
        self.assertTrue(any("Dígitos inválidos" in e for e in errores))

    def test_valor_fuera_de_rango(self):
        respuesta = self.post_conversion("70000", "10")
        errores = respuesta.context["conversion_errores"]
        self.assertEqual(respuesta.context["conversion_resultado"], None)
        self.assertTrue(any("65 535" in e for e in errores))

    def test_valor_negativo(self):
        respuesta = self.post_conversion("-5", "10")
        errores = respuesta.context["conversion_errores"]
        self.assertEqual(respuesta.context["conversion_resultado"], None)
        self.assertTrue(any("negativos" in e for e in errores))

    def test_entrada_vacia(self):
        respuesta = self.post_conversion("", "10")
        errores = respuesta.context["conversion_errores"]
        self.assertTrue(any("ningún número" in e for e in errores))

    # --- Análisis de texto y UTF-8 -------------------------------------------

    def test_texto_con_enye(self):
        respuesta = self.post_texto("ñ")
        self.assertEqual(respuesta.status_code, 200)
        caracteres = respuesta.context["texto_caracteres"]
        self.assertIsNotNone(caracteres)
        self.assertEqual(len(caracteres), 1)
        c = caracteres[0]
        self.assertEqual(c["caracter"], "ñ")
        self.assertEqual(c["decimal"], 241)
        self.assertEqual(c["punto_codigo"], "U+00F1")
        self.assertEqual(c["hexadecimal"], "F1")
        self.assertEqual(c["bytes_utf8"], "C3 B1")

    def test_texto_varios_caracteres(self):
        respuesta = self.post_texto("Hola")
        caracteres = respuesta.context["texto_caracteres"]
        self.assertEqual(len(caracteres), 4)
        self.assertEqual(caracteres[0]["decimal"], 72)  # H
        self.assertEqual(caracteres[0]["bytes_utf8"], "48")

    def test_texto_vacio(self):
        respuesta = self.post_texto("")
        errores = respuesta.context["texto_errores"]
        self.assertTrue(any("ningún texto" in e for e in errores))

    def test_texto_mas_de_20_caracteres(self):
        respuesta = self.post_texto("a" * 21)
        errores = respuesta.context["texto_errores"]
        self.assertTrue(any("20" in e for e in errores))
