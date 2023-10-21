# Calendarizador de Programas UC

Este repositorio alberga una aplicación web capaz de obtener las evaluaciones y fechas de un programa del curso de la UC, para luego crear un calendario en formato .ics que puede ser importado tanto a Google Calendar como a Outlook u otro calendario.

El proyecto combina desarrollo web, extracción de texto y inteligencia artificial para brindar un producto sencillo y automatizado en la creación de calendarios.

**Nota**: El proyecto actualmente está en desarrollo y no se asegura que las fechas generadas por la IA sean fiables, es necesario validar las fechas creadas con precaución.

## Features:

- Obtención automática de eventos y fechas desde un achivo .pdf
- Generación automática de un archivo de calendario .ics a partir de las evaluaciones extraidas

## Instalación:

### Variables de entorno

Se debe crear el archivo `.env` a partir del archivo `.env.example` en el directorio raiz del proyecto, incluyendo una API KEY de OpenAI (Con saldo).

### Ejecución de la App

Para correr la app de forma más sencilla se puede hacer uso de [Docker](https://www.docker.com/get-started/). Los comandos son los siguientes (desde el directorio raiz del repositorio)

```
docker compose build
docker compose up
```

Si se quiere dejar corriendo en segundo plano usar

```
docker compose up -d
```

Una vez corriendo la aplicación se puede ingresar a `http://localhost:3000` para acceder al frontend de la aplicación.

Hay programas del curso de prueba en la carpeta `tests`, se recomeinda usar el archivo `sample.pdf` para ver el funcionamiento

### Desarrollo en local (Sin Docker):

Para desarrollar localmente recomiendo seguir las documentaciones de FastAPI y Vite para poder desarrollar localmente usando hot reloding y otras funcionalidades comodas. Principalmente se deben realizar los siguientes pasos

### Backend

```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```
cd frontend
yarn install
yarn dev
```

Recomiendo fuertemente el uso de un cliente http en consola como [httpie](https://httpie.io/) para hacer solicitudes al back, aunque también pueden usar Postman Reqbin u otro cliente que les acomode.

## Arquitectura:

La app consiste en 2 componentes

1. Backend en Python (FastAPI) para poder hacer el upload y procesado de los archivos y calendarios.
2. Frontend en React (Vite) como aplicación web para la UI de la aplicación.

## Funcionamiento

El flujo consiste en lo siguiente

1. Un usuario ingresa a la app web y sube un archivo `<programa>.pdf` a la apliación
2. Una vez subido el archivo se presiona el boton para generar las fechas
3. En backend se recibe el archivo .pdf y extrae el texto de este
4. Se pasa el texto extraido en varios chunks a OpenAI para poder extraer los nombres y fechas de los eventos en format JSON
5. Se devuelven todos los eventos encontrados por la IA a la aplicación web
6. Ya cargados los eventos encontrados, el usuario debe aceptar todos los eventos que ha generado la herramienta y los envía nuevamente
7. Una vez recibidos los eventos aceptados, el backend genera un archivo .ics de calendario y devuelve el link de descarga
8. El usuario descarga el archivo de calendario y lo importa a su calendar.

## Estrategias usadas hasta ahora para la IA que obtiene los datos.

1. Se usa short learning en el prompting pasado a ChatGPT para que la IA tenga un poco más de contexto a la hora de parsear los nombres y fechas
2. Se utiliza una validación en el JSON y fechas para filtrar todos los elementos del JSON que no tengan una fecha. (Se rechaza si no está en formato ISO de fecha)
3. Se rechaza cualquier output que no sea un JSON
4. Para poder obtener todos los datos de pdfs largos, estos se separan en chunks de menor tamaño

## Por mejorar:

1. Se debe hacer un mejor prompting de ChatGPT para que hayan menos errores a la hora de generar el JSON de fechas (Aún genera errores varias veces)
2. Hay mucho trabajo que hacer en frontend para mejorar la UI

## Posibles Features:

- [ ] Fijar Nombre del Ramo en los eventos creados
- [ ] Permitir subir multiples programas de distintos ramos de una sola vez
- [ ] Permitir la edición de fechas autogeneradas para corregir fechas incorrectas
- [ ] Dar una interfaz visual que permita visualizar el programa del curso para poder validar más facilmente las fechas autogeneradas.

## Tecnologías utilizadas:

- [Docker](https://www.docker.com/) (para la orquestación de la app en conjunto)

### Frontend:

- [Vite](https://vitejs.dev/)
- [React](https://es.react.dev/)

### Backend:

- [FastAPI](https://fastapi.tiangolo.com/) (Como servidor http y de archivos estaticos)
- [OpenAI](https://platform.openai.com/) (Para analisis de texto y extracción de eventos con fecha)
- [PyPDF](https://pypdf.readthedocs.io/en/stable/) (Para extracción de texto desde el PDF)
