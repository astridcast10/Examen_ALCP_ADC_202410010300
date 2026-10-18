#!/usr/bin/env python
"""Punto de entrada de Django para el proyecto analizador."""

import os
import sys


def main():
    """Ejecuta tareas administrativas de Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analizador.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y disponible en el PATH?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
