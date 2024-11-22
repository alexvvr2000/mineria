from pathlib import Path

import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv, to_datetime


def obtener_dataframe(ruta_csv: Path) -> DataFrame:
    datos = read_csv(ruta_csv)
    return datos


def obtener_histograma(
    folder_imagenes: Path, datos: DataFrame, rango: str = "M"
) -> Path:
    datos["inverse_data"] = to_datetime(datos["inverse_data"])

    datos_agrupados = (
        datos["inverse_data"].dt.to_period(rango).value_counts().sort_index()
    )

    plt.bar(
        datos_agrupados.index.astype(str),
        datos_agrupados.values.astype(float),
        width=0.8,
        align="center",
    )
    plt.title(f"Fecha de accidentes agrupados por {rango}")
    plt.xlabel("Fecha")
    plt.ylabel("Frecuencia")

    plt.xticks(rotation=45, ha="right")

    imagen_path = folder_imagenes / f"histograma_accidentes_{rango}.png"
    plt.tight_layout()
    plt.savefig(imagen_path)
    plt.close()

    return imagen_path
