# Evaluación 2 - Software de Geolocalización con Graphhopper

Este proyecto consiste en un script interactivo en Python desarrollado como parte de la evaluación para la certificación DEVNET/DEVASC. El programa utiliza la API de Graphhopper Directions y Geocoding para calcular rutas, distancias, tiempos de viaje y proporcionar instrucciones paso a paso entre dos ubicaciones.

## Características

- Interfaz completamente traducida al español.
- Redondeo y visualización de valores numéricos (distancias y tiempos) a un máximo de dos decimales.
- Opción para finalizar la ejecución ingresando `s` o `salir`.
- Generación de la narrativa detallada del viaje (instrucciones paso a paso) en español.
- Detección prioritaria de ubicaciones dentro de Chile.

## Requisitos

- Python 3.x
- Librería `requests` (`pip install requests`)
- Una clave API (API Key) activa de Graphhopper.

## Instrucciones de Ejecución

1. Clonar este repositorio o descargar el script `geolocalizacion.py`.
2. Asegurarse de tener configurada tu clave API en la variable `key` dentro del archivo Python.
3. Ejecutar el script desde la terminal:

```bash
python3 geolocalizacion.py