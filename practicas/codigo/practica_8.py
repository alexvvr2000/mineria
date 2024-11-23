from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def generar_modelo_lineal_serie_temporal(
    dataframe: pd.DataFrame, carpeta_destino: Path
) -> list[Path]:
    carpeta_destino = Path(carpeta_destino)
    carpeta_destino.mkdir(parents=True, exist_ok=True)
    rutas_imagenes = []

    # Convertir la columna "hour" en un formato datetime
    dataframe["timestamp"] = pd.to_datetime(dataframe["hour"], format="%H:%M:%S")
    dataframe["time_numeric"] = (
        dataframe["timestamp"] - dataframe["timestamp"].min()
    ).dt.total_seconds()

    columnas_numericas = [
        "time_numeric",
        "people",
        "deaths",
        "slightly_injured",
        "severely_injured",
        "uninjured",
        "ignored",
        "total_injured",
        "vehicles_involved",
    ]
    dataframe[columnas_numericas] = dataframe[columnas_numericas].apply(
        pd.to_numeric, errors="coerce"
    )
    dataframe = dataframe.dropna()

    # Variables independientes y dependientes
    X = dataframe[["time_numeric"]]
    y = dataframe["total_injured"]

    # Dividir en conjunto de entrenamiento y prueba
    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Crear y entrenar el modelo
    modelo = LinearRegression()
    modelo.fit(X_entrenamiento, y_entrenamiento)

    # Predicciones
    y_predicho_prueba = modelo.predict(X_prueba)
    y_predicho_entrenamiento = modelo.predict(X_entrenamiento)

    # Métricas
    r2 = r2_score(y_prueba, y_predicho_prueba)
    mse = mean_squared_error(y_prueba, y_predicho_prueba)

    # Guardar los resultados en un archivo
    with open(carpeta_destino / "modelo_lineal_serie_temporal.txt", "w") as archivo:
        archivo.write("Modelo de Regresión Lineal sobre Serie Temporal\n")
        archivo.write(f"Coeficiente: {modelo.coef_[0]}\n")
        archivo.write(f"Intercepto: {modelo.intercept_}\n")
        archivo.write(f"R2 Score: {r2}\n")
        archivo.write(f"Mean Squared Error: {mse}\n")

    # Graficar resultados de prueba
    ruta_grafico_serie = carpeta_destino / "grafico_serie_temporal_prueba.png"
    plt.figure(figsize=(10, 6))
    plt.scatter(
        X_prueba, y_prueba, label="Datos Reales (Prueba)", color="blue", alpha=0.5
    )
    plt.plot(
        X_prueba, y_predicho_prueba, label="Predicción (Prueba)", color="red", alpha=0.7
    )
    plt.xlabel("Tiempo (segundos desde inicio)")
    plt.ylabel("Total de heridos")
    plt.title("Predicción de heridos basada en el tiempo (Prueba)")
    plt.legend()
    plt.savefig(ruta_grafico_serie)
    plt.close()
    rutas_imagenes.append(ruta_grafico_serie)

    # Graficar resultados de entrenamiento
    ruta_grafico_entrenamiento = (
        carpeta_destino / "grafico_serie_temporal_entrenamiento.png"
    )
    plt.figure(figsize=(10, 6))
    plt.scatter(
        X_entrenamiento,
        y_entrenamiento,
        label="Datos Reales (Entrenamiento)",
        color="green",
        alpha=0.5,
    )
    plt.plot(
        X_entrenamiento,
        y_predicho_entrenamiento,
        label="Predicción (Entrenamiento)",
        color="orange",
        alpha=0.7,
    )
    plt.xlabel("Tiempo (segundos desde inicio)")
    plt.ylabel("Total de heridos")
    plt.title("Modelo de entrenamiento basado en el tiempo")
    plt.legend()
    plt.savefig(ruta_grafico_entrenamiento)
    plt.close()
    rutas_imagenes.append(ruta_grafico_entrenamiento)

    return rutas_imagenes
