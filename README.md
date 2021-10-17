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

Beatriz Lozano Ballesteros | Gabriel Romero Fernández

## Descripción de los ficheros

* scraper.properties: fichero de propiedades donde se configura el modo de ejecución del script. 
La ejecución puede ser
  - En modo interactivo: se solicitan los parámetros de entrada para la ejecución del script por la entrada estándar
  - En modo test: los parámetros de entrada para la ejecución del script se leen del fichero de propiedades scraper.properties
* main.py: invoca al scraper según el modo de ejecución configurado en el fichero de propiedades scraper.properties
* scraper.py: realiza las funciones de scraping y guarda los resultados en un fichero en formato csv

## Ejecútame

Utilizando esta sentencia:

python main.py

## DOI de Zenodo

Digital Object Identifier (DOI) de la dataset en Zenodo

https://zenodo.org/record/5574493#.YWxVghpByUk

