from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor


def generar_modelo_knn(dataframe: pd.DataFrame, carpeta_destino: Path) -> list[Path]:
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
    modelo = KNeighborsRegressor(n_neighbors=5)
    modelo.fit(X_entrenamiento, y_entrenamiento)

    y_predicho_prueba = modelo.predict(X_prueba)
    r2 = r2_score(y_prueba, y_predicho_prueba)

    with open(carpeta_destino / "modelo_knn.txt", "w") as archivo:
        archivo.write(f"Modelo KNN: n_neighbors = 5\n")
        archivo.write(f"R2 Score: {r2}\n")

    for columna in X.columns:
        ruta_grafico_columna = (
            carpeta_destino / f"grafico_{columna}_vs_total_heridos.png"
        )
        plt.figure()
        plt.scatter(
            X_prueba[columna], y_prueba, label="Original", alpha=0.5, color="blue"
        )
        plt.scatter(
            X_prueba[columna], y_predicho_prueba, label="Modelo", alpha=0.5, color="red"
        )
        plt.xlabel(columna)
        plt.ylabel("Total de heridos")
        plt.title(f"Comparación de {columna} contra total de heridos (KNN)")
        plt.legend()
        plt.savefig(ruta_grafico_columna)
        plt.close()
        rutas_imagenes.append(ruta_grafico_columna)

    return rutas_imagenes
