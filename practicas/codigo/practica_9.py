from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud


def generar_nube_de_palabras(ruta_salida: Path, dataframe: pd.DataFrame) -> Path:
    if "cause_of_accident" not in dataframe.columns:
        raise ValueError("El DataFrame no contiene la columna 'cause_of_accident'.")

    dataframe = dataframe[dataframe["cause_of_accident"].notnull()]

    texto_causas = " ".join(dataframe["cause_of_accident"])

    nube_palabras = WordCloud(
        width=800, height=400, background_color="white", colormap="viridis"
    ).generate(texto_causas)

    nuevo_archivo = ruta_salida / "word_cloud.png"

    plt.figure(figsize=(10, 5))
    plt.imshow(nube_palabras, interpolation="bilinear")
    plt.axis("off")
    plt.title("Causas de Accidentes", fontsize=16)
    plt.savefig(nuevo_archivo, format="png", dpi=300)
    plt.close()

    return nuevo_archivo
