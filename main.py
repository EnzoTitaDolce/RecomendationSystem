print("La aplicación se está ejecutando...")
from fastapi import FastAPI
from fastapi import Depends
from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
import pandas as pd
import ast
import os

app = FastAPI()
user_data_results = pd.read_csv("funciones/userDataResults.csv")
developer_results = pd.read_csv("funciones/developerResults.csv")
user_for_genre = pd.read_csv("funciones/userForGenreResults.csv")
best_developer_results = pd.read_csv("funciones/bestDeveloperResults.csv")
developer_reviews_results = pd.read_csv("funciones/developerReviewsResults.csv")
recomendaciones_df = pd.read_csv("funciones/recomendaciones.csv")

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de análisis de desarrolladores de juegos"}

@app.get("/developer/{desarrollador}")
async def developer(desarrollador: str = Path(...)):
    # Filtrar los resultados por el desarrollador especificado
    developer_data = developer_results[developer_results['developer'] == desarrollador]
    
    if developer_data.empty:
        return JSONResponse(status_code=404, content={"error": "Desarrollador no encontrado"})

    # Crear un diccionario para almacenar los resultados por año
    resultados_dict = {}
    
    # Iterar sobre cada fila de los datos del desarrollador
    for index, row in developer_data.iterrows():
        year = row['year']
        items_per_year = row['items_per_year']
        free_per_year = row['free_per_year']
        free_per_year_percent = row['free_per_year_percent']

        # Agregar los resultados al diccionario
        resultados_dict[year] = {
            'items_per_year': items_per_year,
            'free_per_year': free_per_year,
            'free_per_year_percent': free_per_year_percent
        }

    return resultados_dict


@app.get("/userdata/{user_id}")
async def userdata(user_id: str = Path(...)):
    
    user_data = user_data_results[user_data_results['user_id'] == user_id]
    
    if user_data.empty:
        return JSONResponse(status_code=404, content={"error": "Usuario no encontrado"})
    
    # Obtener los datos del usuario
    items_count = float(user_data['items_count'].iloc[0])
    total_gastado = float(user_data['Total Gastado'].iloc[0])
    recommend = float(user_data['recommend'].iloc[0])

    # Formatear los resultados
    resultados = {
        "Usuario": user_id,
        "Cantidad_items": items_count,
        "Dinero_gastado": f"{total_gastado} USD",
        "Porcentaje_recomendacion": f"{recommend}%"
    }

    return resultados

@app.get("/userforgenre/{genero}")
async def userforgenre(genero: str = Path(...)):
    # Filtrar los datos por el género especificado
    data = user_for_genre[user_for_genre['genres_x'] == genero]
    
    if data.empty:
        return JSONResponse(status_code=404, content={"error": "Género no encontrado"})
    
    # Encontrar el usuario con más horas jugadas para el género dado
    max_horas_usuario = data.loc[data['playtime_forever_x'].idxmax()]
    usuario_max_horas = max_horas_usuario['user_id']

    # Obtener la acumulación de horas jugadas por año de lanzamiento para el género dado
    acumulacion_horas_por_anio = data.groupby('year')['playtime_forever_y'].sum().reset_index()
    horas_por_anio = [{"Año": row['year'], "Horas": row['playtime_forever_y']} for index, row in acumulacion_horas_por_anio.iterrows()]

    # Formatear los resultados
    resultados = {
        "Usuario con más horas jugadas para género": usuario_max_horas,
        "Horas jugadas": horas_por_anio
    }

    return resultados

@app.get("/bestdeveloperyear/{year}")
async def best_developer_year(year: int = Path(...)):
    # Filtrar los datos por el año especificado
    data = best_developer_results[best_developer_results['year'] == year]
    
    print(data)
    if data.empty:
        return JSONResponse(status_code=404, content={"error": "Año no encontrado"})
    # Limpiar los nombres de los desarrolladores
    data['developer'] = data['developer'].str.strip()  # Eliminar espacios en blanco al principio y al final
      
    # Calcular el top 3 de desarrolladores con más juegos recomendados
    top_desarrolladores = data['developer'].value_counts().nlargest(3)

    # Formatear los resultados
    resultados = {
        "Año": year,
        "Top 3 de desarrolladores": top_desarrolladores.to_dict()
    }

    return resultados

@app.get("/developerreviewsanalysis/{desarrolladora}")
async def developer_reviews_analysis(desarrolladora: str = Path(...)):
    # Filtrar los datos por la desarrolladora especificada
    data = developer_reviews_results[developer_reviews_results['developer'] == desarrolladora]
    print(data)
    if data.empty:
        return JSONResponse(status_code=404, content={"error": "Desarrolladora no encontrada"})

    # Contar la cantidad de registros categorizados como análisis de sentimiento positivo y negativo
    positive_count = (data['sentiment_analysis'] == 2).sum()
    negative_count = (data['sentiment_analysis'] == 0).sum()

    # Crear el diccionario de resultados
    resultados = {
        desarrolladora: {"Positive": int(positive_count), "Negative": int(negative_count)}
    }

    return resultados

@app.get("/recomendacion_juego/{id_producto}")
async def recomendacion_juego(id_producto: int = Path(...)):
    # Buscar las recomendaciones para el ID de producto especificado
    recomendaciones = recomendaciones_df[recomendaciones_df['id'] == id_producto]['recommendations'].values
    print(recomendaciones)
    if len(recomendaciones) == 0:
        return JSONResponse(status_code=404, content={"error": "ID de producto no encontrado"})
    
    # Convertir la cadena de recomendaciones a una lista de Python
    recomendaciones = ast.literal_eval(recomendaciones[0])
    
    # Limitar a las primeras 5 recomendaciones si hay más
    recomendaciones = recomendaciones[:5]
    
    return {"id_producto": id_producto, "recomendaciones": recomendaciones}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)