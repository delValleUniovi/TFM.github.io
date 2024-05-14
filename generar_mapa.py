from bs4 import BeautifulSoup
import folium

# Lee el archivo XML
with open('nuevo1.xml', 'r') as file:
    data = file.read()

# Analiza el XML sin especificar el analizador, para que BeautifulSoup elija automáticamente
soup = BeautifulSoup(data, features='xml')

# Encuentra la etiqueta de coordenadas
coordenadas = soup.find('coordenadas')

# Encuentra todas las etiquetas de punto dentro de coordenadas
puntos = coordenadas.find_all('punto')

# Crear un diccionario para almacenar las coordenadas y la información asociada
coordenadas_info = {}

# Itera sobre las etiquetas de punto y agrupa la información por coordenadas
for punto in puntos:
    latitud = float(punto.find('latitud').text)
    longitud = float(punto.find('longitud').text)
    leyenda = punto.find('leyenda').text if punto.find('leyenda') else ''  # Si la etiqueta leyenda existe, obtén su texto, de lo contrario, usa una cadena vacía
    
    # Agrega la información al diccionario usando las coordenadas como clave
    if (latitud, longitud) not in coordenadas_info:
        coordenadas_info[(latitud, longitud)] = {}
    
    # Incrementa el contador de la leyenda para las coordenadas dadas
    coordenadas_info[(latitud, longitud)][leyenda] = coordenadas_info[(latitud, longitud)].get(leyenda, 0) + 1

# Crea un mapa
mymap = folium.Map(location=[0, 0], zoom_start=3)

# Itera sobre las coordenadas y la información asociada y agrega marcadores al mapa
for coordenadas, info in coordenadas_info.items():
    latitud, longitud = coordenadas
    # Construye el texto del tooltip del marcador
    tooltip_text = '<br>'.join([f'{leyenda}: {cantidad}' for leyenda, cantidad in info.items()])
    folium.Marker(location=[latitud, longitud], tooltip=tooltip_text).add_to(mymap)

# Guarda el mapa como un archivo HTML
mymap.save("mapa.html")