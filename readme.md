#Proyecto Data Science#
##Sistema de Recomendación##
##Autor: Enzo Giancarlo Tita Dolce##
###Fecha: 07/02/2024##

##Introducción##
En este proyecto analizcé un conjunto de datos de la compañía Steam.
Dichos datos están distribuidos en 3 datasets contienen información sobre: 
-Los juegos que están/estuvieron en la plataforma, como ser, la empresa desarrolladora, el precio, el género, etc.
-Los usuarios registrados, como ser, los productos adquiridos, la cantidad de horas dedicadas a cada juego,etc
-Las reseñas que los usuarios hicieron sobre los distintos juegos que adquirieron

##Desarrollo##
Para llevar a cabo el trabajo utilizcé las librerías estandar para el procesamiento de datos (pandas, numpy, matplotlib, etc)  y algunas específicas para el modelo de recomendación (scikit-learn), ntlk para el procesamiento de las reseñas y otras como ast para convertir strings en listas, entre otras.

###Preparación de archivos###
El notebook llamado exploracion_archivos contiene todo el trabajo necesario para poder extraer los datos de los datasets. En ese notebook extraigo los datos de los archivos en formato gz y los convierto a un dataframe, desanido las listas y diccionarios que correspondan y hago el análisis de las reseñas asignandoles un puntaje de 2 para las positivas, 1 para las neutrales y ausentes y 0 para las negativas.
Básicamente, en este notebook preparo los dataframes para que queden listos para usarse en las funciones y analizarse para el EDA.

Dentro de la carpeta funciones están los notebook correspondientes a cada endpoint y sus resultados en formato csv.

Para recrear el trabajo de este proyecto solo es necesario descargar el repositorio, guardar los archivos gz del dataset en el mismo directorio que el notebook exploracion_archivos, crear la carpeta funciones en el mismo directorio y colocar los otros notebooks dentro de esa carpeta. Los archivos csv intermedios que se crearon durante la preparación de los datasets se crearán automaticamente y serviran de fuente de datos limpios para los notebooks de las funciones que, a su vez, crearán los archivos con los resultados que servirán para la api.

El EDA no fue tan profundo como me hubiera gustado por una cuestión de tiempo. Tuve muchos problemas con el deploy y por eso lo resigné un poco. Podría decirse que está a medio camino.
