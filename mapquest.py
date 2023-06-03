#	USO DE API PÚBLICA

#	LIBRERÍAS
import urllib.parse, requests
import time

# VARIABLES
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "Cj7Vt7i2oSy0Wtl1Kz1mKBp1fj47R6WW"
hlocal = time.strftime("%H:%M")

while True :

#	MENSAJE DE BIENVENIDA

	print("\nBienvenido al portal de consultas\n", hlocal)

#	SOLICITUD DE ORIGEN Y DESTINO PARA REALIZAR EL CÁLCULO

	orig = input("\nIndique su ciudad de origen: ")
	if orig == "exit":
		print("Saliendo del programa...\n")
		break

	dest = input("\nIndique su ciudad de destion: ")
	if dest == "exit":
		print("Saliendo del programa...\n")
		break

#	SOLICITUD HACIA LA API Y VARIABLES JSON

	url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest, "locale": "es_ES"})
	print("URL: " + url)
	json_data = requests.get(url).json()
	json_status = json_data ["info"] ["statuscode"]

#	CÁLCULO DE DISTANCIA  Y TIEMPO SEGÚN DATOS OTORGADOS

	if json_status == 0:
		print ("Código de estado de API = " + str(json_status) + " = Llamada de ruta exitosa.\n")
		print ("==================================================")
		print ("Dirección desde " + orig + " hasta " + dest)
		print ("Duración del viaje estimada: " + json_data["route"]["formattedTime"])
		print ("Kilómetros totales: {:.4f}".format(json_data["route"]["distance"] * 1.61))

#	CÁLCULO DE COMBUSTIBLE SEGÚN DATOS OTORGADOS

		if "fuelUsed" in json_data["route"]:
			print("Fuel Used (Ltr): {:.4F}".format(json_data["route"]["fuelUsed"] * 3.78))
		else:
			print("La información sobre combustibles se encuentra obsoleta.")
		print ("==================================================")

#	NARRATIVA DE RUTA IDENTIFICADA POR EL PROGRAMA

		for each in json_data["route"]["legs"][0]["maneuvers"]:
			dist_km = each["distance"] * 1.61
			print (each ["narrative"] + "({:.4f} km)".format(dist_km))
		print ("==================================================\n")
		break

#	PROPORCIONA INFORMACIÓN DE OTROS CÓDIGOS DE ESTADO

	elif json_status == 402:
		print ("==================================================")
		print ("Código de estado: " + str(json_status) + "; Solicitud inválida para una o ambas ubicaciones.")
		print ("==================================================\n")
		break
	else:
		print ("==================================================")
		print ("Para el código de estado: " + str(json_status) + "; referirse al enlace: ")
		print ("https://developer.mapquest.com/documentation/directions-api/status-codes")
		print ("==================================================\n")
		break

	break
