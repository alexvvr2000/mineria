from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def lista_visualizaciones(df: pd.DataFrame, output_folder: Path) -> List[Path]:
    output_folder.mkdir(parents=True, exist_ok=True)

    rutas_generadas = []

    plt.figure(figsize=(12, 8))
    plt.scatter(df["total_injured"], df["vehicles_involved"], alpha=0.5, c="blue")
    plt.title(
        "Gráfico de dispersión: Total de heridos vs Vehículos involucrados", fontsize=16
    )
    plt.xlabel("Total de heridos", fontsize=14)
    plt.ylabel("Vehículos involucrados", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=45, ha="right")
    ruta_dispercion = output_folder / "grafico_dispercion.png"
    plt.tight_layout()
    plt.savefig(ruta_dispercion)
    rutas_generadas.append(ruta_dispercion)
    plt.close()

    plt.figure(figsize=(12, 8))
    sns.boxplot(x="victims_condition", y="total_injured", data=df)
    plt.title(
        "Diagrama de caja: Condición de víctimas vs Total de heridos", fontsize=16
    )
    plt.xlabel("Condición de víctimas", fontsize=14)
    plt.ylabel("Total de heridos", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=45, ha="right")
    ruta_caja = output_folder / "diagrama_caja.png"
    plt.tight_layout()
    plt.savefig(ruta_caja)
    rutas_generadas.append(ruta_caja)
    plt.close()

    return rutas_generadas
