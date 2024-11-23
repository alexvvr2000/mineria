from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


def generar_modelo_kmeans(dataframe: pd.DataFrame, carpeta_destino: Path) -> list[Path]:
    carpeta_destino = Path(carpeta_destino)
    carpeta_destino.mkdir(parents=True, exist_ok=True)
    rutas_imagenes = []

    dataframe["hora"] = pd.to_datetime(dataframe["hour"], format="%H:%M:%S").dt.hour
    dataframe = dataframe.replace(",", ".", regex=True)
    columnas_numericas = [
        "inverse_data",
        "hora",
        "km",
        "people",
        "deaths",
        "slightly_injured",
        "severely_injured",
        "uninjured",
        "ignored",
        "total_injured",
        "vehicles_involved",
        "latitude",
        "longitude",
    ]
    dataframe[columnas_numericas] = dataframe[columnas_numericas].apply(
        pd.to_numeric, errors="coerce"
    )

    dataframe = dataframe.dropna()
    X = dataframe[["hora", "km", "people", "vehicles_involved"]]
    y = dataframe["total_injured"]

    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Se que K debe varaibr pero este es un valor de ejemplo
    n_clusters = 5
    modelo = KMeans(n_clusters=n_clusters, random_state=42)
    modelo.fit(X_entrenamiento)

    y_predicho_entrenamiento = modelo.predict(X_entrenamiento)
    y_predicho_prueba = modelo.predict(X_prueba)

    r2_entrenamiento = r2_score(y_entrenamiento, y_predicho_entrenamiento)
    r2_prueba = r2_score(y_prueba, y_predicho_prueba)

    with open(carpeta_destino / "modelo_kmeans.txt", "w") as archivo:
        archivo.write(f"Modelo K-Means: n_clusters = {n_clusters}\n")
        archivo.write(f"R2 Score (entrenamiento): {r2_entrenamiento}\n")
        archivo.write(f"R2 Score (prueba): {r2_prueba}\n")

    for columna in X.columns:
        ruta_grafico_columna = (
            carpeta_destino / f"grafico_{columna}_vs_total_heridos.png"
        )
        plt.figure()
        plt.scatter(
            X_prueba[columna], y_prueba, label="Original", alpha=0.5, color="blue"
        )
        plt.scatter(
            X_prueba[columna],
            y_predicho_prueba,
            label="Cluster",
            alpha=0.5,
            color="red",
        )
        plt.xlabel(columna)
        plt.ylabel("Total de heridos")
        plt.title(f"Comparación de {columna} contra total de heridos (K-Means)")
        plt.legend()
        plt.savefig(ruta_grafico_columna)
        plt.close()
        rutas_imagenes.append(ruta_grafico_columna)

    return rutas_imagenes
