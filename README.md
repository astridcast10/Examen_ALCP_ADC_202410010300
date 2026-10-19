# Analizador de representación de datos

Aplicación web con Python y Django para convertir números entre bases y analizar texto en UTF-8.

## ¿Qué hace?

Tiene dos formularios:

1. Conversión de números: ingresa un número y elige su base de origen 2, 8, 10 o 16. Valida los dígitos, revisa que esté entre 0 y 65 535 y muestra el resultado en decimal, binario, octal y hexadecimal, junto con los bits significativos y bytes necesarios.

2. Análisis de texto: acepta hasta 20 caracteres. Para cada letra muestra el carácter, su código decimal, el punto U, el valor hexadecimal y sus bytes en UTF-8.

## Ejecutar localmente

Entra a la carpeta del proyecto:

```
cd analizador_representacion_datos
```

Instala las dependencias:

```
pip install -r requirements.txt
```

Ejecuta el servidor:

```
python manage.py runserver
```

Abre http://localhost:8000 en el navegador.

## Pruebas

Ejecuta las pruebas automatizadas:

```
python manage.py test
```

## Docker

Construye la imagen:

```
docker build -t analizador-datos .
```

Ejecuta con Docker Compose:

```
docker compose up --build
```

La aplicación queda disponible en http://localhost:8000.

Ejecuta con límites de 256 MB de memoria y 1 CPU:

```
docker run --rm --name analizador-datos --memory=256m --cpus=1 -p 8000:8000 analizador-datos
```

Ver el consumo de recursos:

```
docker stats analizador-datos --no-stream
```
