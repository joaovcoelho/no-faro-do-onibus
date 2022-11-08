import requests
from time import sleep
import folium
from folium import plugins

inicio = "\033[1;33;41m"+ """
   No Faro do Ônibus   \033[m\n
Buscador de ônibus do RJ em tempo real.
Desenvolvido por:  João V. Coelho
19/07/2022 \n
"""
print(inicio)



# url = "https://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/onibus/"
url ="https://jeap.rio.rj.gov.br/dadosAbertosAPI/v2/transporte/veiculos/onibus/"

# Função para depuração de request
def DEBUG():
	response = requests.get(url+"821")
	response_json = response.json()
	print(response_json)

#DEBUG()

busca = int(input("Que linha deseja buscar? \n   ==> "))
url_busca = url + str(busca)


# Realiza a rotina 20x, com intervalo de 12s/cada
for rotina in range(20):
	# Recebe e armazena os carros rodando
	response = requests.get(url_busca)
	response_json = response.json()
	#print(response_json)
	
	# Cria mapa base
	latitude, longitude = response_json["data"][0][3:5]
	
	mapa = folium.Map(location=[latitude, longitude], tiles='OpenStreetMap', zoom_start=13)
	
	
	# Faz a separação dos carros em uma lista
	print()
	carros = []
	for indice, carro in enumerate(response_json["data"]):
		numero = carro[1]
		latitude = carro[3]
		longitude = carro[4]
		velocidade = carro[5]
		
		# Direção do carro
		if carro[6] == '': angulo = 0
		else: angulo = int(carro[6]) 
		
		print(f"{indice+1}  | Encontrado carro número: {numero}")
		
		dados_carro = (numero, latitude, longitude, velocidade, angulo)
		carros.append(dados_carro)
		
		# Cria marcadores e insere rotulos
		rotulo = f"<h4>{numero}</h4> <br> {velocidade} km/h <br> Direção: {angulo}°"
		fg = folium.FeatureGroup(name="fg_carros")
		
		# Cria marcador direcional personalizado
		fg.add_child(folium.Marker(location=[latitude, longitude],popup=rotulo, icon=folium.Icon(icon="arrow-up", color="orange", angle=angulo)))
		
		#fg.add_child(plugins.SemiCircle(location=[latitude, longitude], radius=700, popup=rotulo, fill = True,fill_color="orange", fill_opacity=0.9, color="black", start_angle=(angulo+180)-30, stop_angle=(angulo+180)+30))
		
		# Insere marcador no mapa
		mapa.add_child(fg)
	
	
	# Gera HTML com as posições
	mapa.save("index.html")
	sleep(12)

	