import os
from flask import Flask, render_template
from bs4 import BeautifulSoup
import folium

app = Flask(__name__)

@app.route('/')
def index():
    # Lee el archivo XML
    xml_file = 'nuevo1.xml'
    with open(xml_file, 'r') as file:
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

    # Guarda el mapa como un archivo HTML en el directorio 'static'
    mapa_file = 'mapa.html'  # Ruta relativa al directorio 'static'
    mapa_abs_path = os.path.join('static', mapa_file)  # Ruta absoluta del archivo HTML

    # Guarda el mapa
    mymap.save(mapa_abs_path)

    # Renderiza la plantilla HTML y pasa la ruta del archivo mapa.html
    return render_template('index.html', mapa_path=mapa_file)

if __name__ == '__main__':
    app.run(debug=True)