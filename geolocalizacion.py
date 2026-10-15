import urllib.parse
import requests

# URL base de la API de Graphhopper Directions
route_url = "https://graphhopper.com/api/1/route?"

# Clave API de Graphhopper configurada
key = "b5190ef5-e438-423d-80b4-ff005663180c"


def geocoding(location, key):
  """Obtiene las coordenadas latitud y longitud a partir de un nombre de ubicación."""
  geocode_url = "https://graphhopper.com/api/1/geocode?"
  url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
  reply = requests.get(url)
  json_data = reply.json()
  json_status = reply.status_code

  if json_status == 200 and len(json_data["hits"]) != 0:
    lat = json_data["hits"][0]["point"]["lat"]
    lng = json_data["hits"][0]["point"]["lng"]
    nombre_formateado = json_data["hits"][0]["name"]
    if "country" in json_data["hits"][0]:
      nombre_formateado += ", " + json_data["hits"][0]["country"]
    return json_status, lat, lng, nombre_formateado
  else:
    return json_status, None, None, location


while True:
  print("\n" + "=" * 60)
  print("=== SISTEMA DE GEOLOCALIZACIÓN Y RUTAS (GRAPHHOPPER) ===")
  print("=" * 60)

  loc1 = input(
      "\nIngrese la ciudad o ubicación de ORIGEN (o 's'/'salir' para"
      " terminar): "
  )
  if loc1.lower().strip() in ["s", "salir", "quit", "q"]:
    print("\n¡Gracias por utilizar el sistema de geolocalización! Hasta luego.")
    break

  loc2 = input(
      "Ingrese la ciudad o ubicación de DESTINO (o 's'/'salir' para"
      " terminar): "
  )
  if loc2.lower().strip() in ["s", "salir", "quit", "q"]:
    print("\n¡Gracias por utilizar el sistema de geolocalización! Hasta luego.")
    break

  # Obtención de coordenadas para el origen
  status1, lat1, lng1, orig_nombre = geocoding(loc1, key)
  if status1 != 200 or lat1 is None:
    print(f"\n[ERROR] No se pudo encontrar la ubicación de origen: '{loc1}'")
    continue

  # Obtención de coordenadas para el destino
  status2, lat2, lng2, dest_nombre = geocoding(loc2, key)
  if status2 != 200 or lat2 is None:
    print(f"\n[ERROR] No se pudo encontrar la ubicación de destino: '{loc2}'")
    continue

  print("\n" + "-" * 60)
  print(f"Origen confirmado:  {orig_nombre} (Lat: {lat1:.2f}, Lng: {lng1:.2f})")
  print(f"Destino confirmado: {dest_nombre} (Lat: {lat2:.2f}, Lng: {lng2:.2f})")
  print("-" * 60)

  # Parámetros para la solicitud de ruta ('locale=es' fuerza las instrucciones en español)
  query_params = [
      ("point", f"{lat1},{lng1}"),
      ("point", f"{lat2},{lng2}"),
      ("vehicle", "car"),
      ("locale", "es"),
      ("key", key),
  ]

  url = route_url + urllib.parse.urlencode(query_params)
  reply = requests.get(url)
  json_status = reply.status_code
  json_data = reply.json()

  if json_status == 200 and "paths" in json_data:
    path = json_data["paths"][0]

    # Cálculos numéricos con formato a 2 decimales
    distancia_km = path["distance"] / 1000.0  # Convertir metros a kilómetros
    distancia_mi = distancia_km * 0.621371  # Convertir a millas

    tiempo_ms = path["time"]
    horas = int(tiempo_ms // (1000 * 60 * 60))
    minutos = int((tiempo_ms % (1000 * 60 * 60)) // (1000 * 60))
    segundos = (tiempo_ms % (1000 * 60)) / 1000.0

    print("\n--- RESUMEN DEL VIAJE ---")
    print(
        f"Distancia total: {distancia_km:.2f} km ({distancia_mi:.2f} millas)"
    )
    print(
        f"Tiempo estimado:  {horas} hrs, {minutos} min, {segundos:.2f} seg"
    )

    # Narrativa paso a paso del viaje en español
    print("\n--- INSTRUCCIONES PASO A PASO (NARRATIVA) ---")
    instrucciones = path.get("instructions", [])

    for idx, paso in enumerate(instrucciones, start=1):
      texto_paso = paso.get("text", "")
      dist_paso_km = paso.get("distance", 0) / 1000.0
      print(f"{idx}. {texto_paso} ({dist_paso_km:.2f} km)")

    print("-" * 60)
  else:
    print(
        f"\n[ERROR] No se pudo calcular la ruta. Código de estado:"
        f" {json_status}"
    )
    if "message" in json_data:
      print(f"Detalle: {json_data['message']}")
