# Analizador de representación de datos

Aplicación web desarrollada con **Python 3.12+ y Django** que relaciona los sistemas numéricos, la codificación de caracteres y la ejecución en contenedores.

## ¿Qué hace la aplicación?

Tiene dos formularios independientes:

1. **Conversión de sistemas numéricos**: ingresa un número y selecciona su base de origen (2, 8, 10 o 16). La aplicación valida los dígitos, comprueba que el valor esté entre 0 y 65 535, y muestra el resultado en decimal, binario (rellenado al siguiente límite de byte: 8, 16, 24 bits…), octal y hexadecimal, junto con la cantidad de bits significativos y bytes necesarios.
2. **Análisis de texto y UTF-8**: acepta un texto de hasta 20 caracteres. Para cada carácter muestra: el carácter, su código decimal, el punto de código `U+`, el valor hexadecimal y sus bytes en UTF-8.

Se presentan mensajes de error claros para: entrada vacía, dígitos inválidos para la base, valores negativos y valores fuera del rango.

## Estructura del repositorio

```
analizador_representacion_datos/
├── manage.py                 # Entrypoint de Django
├── requirements.txt          # Dependencias (Django==6.0.7)
├── Dockerfile                # Imagen basada en python:3.12-slim
├── compose.yaml              # Despliegue con Docker Compose (puerto 8000, 256 MB RAM, 1 CPU)
├── README.md                 # Este archivo
├── .gitignore
├── analizador/               # Configuración del proyecto Django (settings, urls, wsgi, asgi)
└── conversor/                # App de Django
    ├── forms.py              # Formularios y validación
    ├── views.py              # Lógica de conversiones y análisis UTF-8
    ├── urls.py
    ├── tests.py              # 15 pruebas automatizadas
    └── templates/conversor/index.html
```

## Requisitos

- Python 3.12 o superior (se probó con Python 3.14 y Django 6.0.7)
- Para `--foto` no aplica (no usa Pillow); solo se necesita Django.

## Ejecución local (sin Docker)

```powershell
# Entrar a la carpeta del proyecto
cd analizador_representacion_datos

# Crear entorno virtual (opcional pero recomendado)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor de desarrollo en http://localhost:8000
python manage.py runserver
```

Luego abre `http://localhost:8000` en el navegador.

## Pruebas automatizadas

El repositorio incluye 15 pruebas (más que las 6 requeridas) que cubren conversiones válidas (binario, octal, decimal, hexadecimal, límite 65 535 y cero), errores de base o rango, valores negativos, entrada vacía y un caso UTF-8 con `ñ`.

```powershell
python manage.py test
```

Resultado esperado: `Ran 15 tests ... OK`.

## Docker y Docker Compose

La imagen está basada en `python:3.12-slim` y expone la aplicación en el puerto 8000.

### Construir la imagen

```powershell
docker build -t analizador-datos .
```

### Ejecutar con Docker Compose (puerto 8000, 256 MB RAM y 1 CPU)

```powershell
docker compose up --build
```

La aplicación quedará disponible en `http://localhost:8000`.

### Ejecutar con `docker run` y límites de recursos

```powershell
docker run --rm --name analizador-datos --memory=256m --cpus=1 -p 8000:8000 analizador-datos
```

### Evidencia de `docker stats`

En otra terminal, mientras el contenedor se ejecuta:

```powershell
docker stats analizador-datos --no-stream
```

Ejemplo de salida esperada (los valores varían según el uso real):

```
CONTAINER ID   NAME              CPU %   MEM USAGE / LIMIT   MEM %   NET I/O     BLOCK I/O   PIDS
abc123def456   analizador-datos  0.15%   45.2MiB / 256MiB    17.6%   64kB / 0B   0B / 0B     12
```

> **Nota:** en este entorno no está instalado Docker, por lo que no pude ejecutar el contenedor ni capturar la evidencia de `docker stats` aquí. Ejecuta los comandos anteriores en tu máquina y adjunta la captura de pantalla de `docker stats` al repositorio o al reporte.

## Arquitectura de Von Neumann — recursos que usa la aplicación

La aplicación se ejecuta como un **programa almacenado** sobre la arquitectura de Von Neumann:

1. **Unidad de procesamiento (CPU):** la unidad de control y la ALU ejecutan las instrucciones del intérprete de Python y del framework Django (gestión de peticiones HTTP, validación de formularios, conversiones de base y análisis UTF-8).
2. **Memoria principal (RAM):** almacena el programa Django mientras se ejecuta y los datos de cada petición (el número a convertir, el texto, los resultados intermedios). En el contenedor esta memoria está limitada a 256 MB.
3. **Entrada:** los formularios web enviados por HTTP desde el navegador (número, base de origen, texto).
4. **Salida:** las respuestas HTTP renderizadas en HTML que se muestran en el navegador del usuario.
5. **Almacenamiento secundario:** el disco del host/contenedor guarda el código fuente, `requirements.txt`, el `Dockerfile` y la imagen del contenedor.

## ¿Por qué el contenedor comparte el kernel del host?

Los contenedores no son máquinas virtuales: no emulan hardware ni traen un sistema operativo invitado completo. Utilizan **virtualización a nivel de sistema operativo** mediante *namespaces* (aislamiento de procesos, red, montajes, etc.) y *cgroups* (límites de CPU y memoria) del propio sistema operativo.

Por eso:

- La imagen `python:3.12-slim` solo trae los binarios y librerías de Python, no un kernel propio.
- El contenedor **usa directamente el kernel del host** (Linux en el caso de Docker Desktop/servidor Linux).
- Al compartir el kernel, el contenedor arranca casi instantáneamente, consume pocos recursos y puede aplicar directamente los límites de 256 MB de RAM y 1 CPU solicitados.

## Entregables pendientes (del estudiante)

1. **Repositorio en GitHub:** subir este proyecto y compartir el enlace público (ver pasos más abajo).
2. **Video (máximo 2 minutos):** debe mostrar, como mínimo:
   - una conversión válida (por ejemplo, `FF` en base 16 → 255 decimal, `11111111` binario, 8 bits, 1 byte);
   - un error de validación (por ejemplo, ingresar `2` en base 2 o `70000` en decimal);
   - un texto con `ñ` (mostrar `U+00F1` y bytes UTF-8 `C3 B1`);
   - ejecución de las pruebas (`python manage.py test`);
   - el contenedor en ejecución y la evidencia de `docker stats`.

## Subir el repositorio a GitHub

```powershell
cd analizador_representacion_datos
git init
git add .
git commit -m "Analizador de representación de datos: conversiones, UTF-8, pruebas y Docker"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/analizador-datos.git
git push -u origin main
```

Reemplaza `TU_USUARIO` por tu usuario de GitHub y crea primero el repositorio vacío en [github.com](https://github.com) sin README para evitar conflictos.
