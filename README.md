# Proyecto de Servicio Web para Procesamiento de Archivos y Consultas a APIs de MercadoLibre

Este proyecto consiste en un servicio web desarrollado con FastAPI que permite procesar archivos de diferentes formatos (CSV, JSONL, TXT) y consultar APIs públicas de MercadoLibre para obtener datos adicionales y almacenarlos en una base de datos.

## Características Principales

- **Procesamiento de Archivos**: Soporte para archivos en formatos `csv`, `jsonl`, y `txt`.
- **Consulta a APIs de MercadoLibre**: Realiza consultas a los endpoints públicos de MercadoLibre para obtener datos adicionales.
- **Almacenamiento en Base de Datos**: Los datos obtenidos del archivo y las consultas a las APIs se almacenan en una base de datos.

## Requisitos

### Software Necesario

- **Python**: Es necesario tener Python instalado.
- **Docker**: La aplicación se ejecuta con Docker, por lo que debes tener Docker y Docker Compose instalados en tu máquina.

### Dependencias de Python

Las dependencias de Python están especificadas en el archivo `requirements.txt`. Si deseas instalarlas manualmente, puedes usar el siguiente comando:

```sh
pip install -r requirements.txt
```

Sin embargo, la recomendación es usar Docker para simplificar la instalación y ejecución.

## Ejecución del Proyecto con Docker

### Construir la Imagen Docker

Desde la raíz del proyecto, ejecuta el siguiente comando para construir la imagen de Docker:

```sh
docker-compose build
```

## Levantar los Contenedores

Una vez construida la imagen, levanta los contenedores de la aplicación y la base de datos con:

```sh
docker-compose up
```

## Acceso al servicio

El servicio web estará disponible en `http://localhost:8000`

## Uso del Endpoint principal

El endpoint principal de la app es:

- **POST** `/file`:

Permite subir un archivo en `cvs`, `jsonl`, o `txt` para ser procesado. El archivo será leido, se consultarán
las APIS de Mercado Libre para obtener información adicional, y los datos se almacenarán en la base de datos MongoDB.

Ejemplo de uso del endpoint con `curl`:

```sh
curl -X POST "http://localhost:8000/file" -F "file=@path/to/your/file.csv"
```

## Estructura del proyecto

La estructura del proyecto sigue los principios SOLID para garantizar un código limpio y modular.  
La organización de las carpetas es la siguiente:

```ssh
app/
    ├── config/
    │   ├── __init__.py
    │   └── config.py          # Configuraciones generales de la app
    ├── database/
    │   ├── __init__.py
    │   └── db.py              # Conexión a la base de datos
    ├── file_reader/
    │   ├── __init__.py
    │   ├── base.py            # Clase base para leer archivos
    │   ├── cvs_read.py        # Lector de archivos CSV
    │   ├── jsonl_read.py      # Lector de archivos JSONL
    │   ├── read_file.py       # Controlador para leer diferentes formatos
    │   └── txt_read.py        # Lector de archivos TXT
    ├── models/
    │   ├── __init__.py
    │   └── models.py          # Modelos de datos
    ├── services/
    │   ├── item_processor.py  # Procesamiento de datos de los items
    │   └── ml_api.py          # Servicio para interactuar con las APIs de MercadoLibre
    ├── main.py                # Punto de entrada principal con el endpoint `/file`
