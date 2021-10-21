# Eating, Drinking & Data Mining


Es un proyecto realizado en el contexto de la asignatura *Tipología y ciclo de vida de los datos*, perteneciente
al *Máster en Ciencia de Datos* de la *Universitat Oberta de Catalunya*.
Este proyecto surge, por tanto, como respuesta a la *Práctica 1* de dicha asignatura, en la que se busca que el 
alumno aprenda a identificar los datos relevantes para un proyecto analítico y a utilizar herramientas de 
extracción de datos.

En **Eating, drinking & data mining**, hemos generado una aplicación en lenguaje de programación *python*, en la que 
partiendo del nombre de una ciudad, se nos genere un dataset conteniendo todos los restaurantes de ese núcleo
poblacional así como sus atributos más interesantes para aplicar minería de datos: horarios de apertura, tipo de
cocina, número de comentarios en redes sociales, etc.

Los datos se han extraído de la web [restaurantguru.com](https://restaurantguru.com/)

![image](https://user-images.githubusercontent.com/92667730/137620094-94f98884-0130-427a-b91b-d1dba5225d3d.png)


## Miembros del equipo

- Beatriz Lozano Ballesteros
- Gabriel Romero Fernández

## Descripción de los ficheros

- **src/scraper.properties**: fichero de propiedades donde se configura el modo de ejecución del script. 
La ejecución puede ser
  - En modo interactivo: se solicitan los parámetros de ejecución del script por pantalla
  - En modo test: se leen los parámetros de ejecución del script de la sección Test del fichero de propiedades
- **src/main.py**: invoca al scraper según el modo de ejecución configurado en el fichero de propiedades scraper.properties
- **src/scraper.py**: realiza las funciones de scraping y guarda los resultados en un fichero en formato csv

## Ejecútame

Utilizando esta sentencia:

python main.py

**Nota**: Si en la ejecución se indica que se habilite el auto scroll, se llamará a webdriver de la librería Selenium. En este caso, será necesario tener en el path el driver  chromedriver.exe, que se puede descargar en la siguiente dirección: https://sites.google.com/chromium.org/driver/

## DOI de Zenodo

Digital Object Identifier (DOI) del dataset en Zenodo:

https://doi.org/10.5281/zenodo.5585051

