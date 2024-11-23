from pathlib import Path

import pandas as pd
from scipy import stats


def ejecutar_anova_ttest(df: pd.DataFrame, carpeta_salida: Path) -> Path:
    df["week_day"] = df["week_day"].str.lower()

    df["km"] = df["km"].str.replace(",", ".", regex=False)
    df["km"] = pd.to_numeric(df["km"], errors="coerce")
    df = df.dropna(subset=["km"])

    archivo_salida = carpeta_salida / "resultados_anova_ttest.txt"

    with open(archivo_salida, "w") as f:
        f.write("ANOVA y T-test - Resultados\n")
        f.write("=================================\n\n")

        f.write("1. ANOVA: km vs semana_dia\n")
        grupos_km = df.groupby("week_day")["km"].apply(list)

        if len(grupos_km) > 1:
            resultado_anova_km = stats.f_oneway(*grupos_km)
            f.write(f"Estadístico F: {resultado_anova_km.statistic}\n")
            f.write(f"Valor p: {resultado_anova_km.pvalue}\n\n")
        else:
            f.write("No se puede realizar ANOVA: No hay suficientes grupos\n\n")

        f.write("2. ANOVA: tipo_carretera vs total_lesionados\n")
        grupos_road_type = df.groupby("road_type")["total_injured"].apply(list)
        resultado_anova_road_type = stats.f_oneway(*grupos_road_type)
        f.write(f"Estadístico F: {resultado_anova_road_type.statistic}\n")
        f.write(f"Valor p: {resultado_anova_road_type.pvalue}\n\n")

        f.write("3. ANOVA: condicion_meteorologica vs total_lesionados\n")
        grupos_weather_condition = df.groupby("wheather_condition")[
            "total_injured"
        ].apply(list)
        resultado_anova_weather = stats.f_oneway(*grupos_weather_condition)
        f.write(f"Estadístico F: {resultado_anova_weather.statistic}\n")
        f.write(f"Valor p: {resultado_anova_weather.pvalue}\n\n")

        f.write("4. T-test: condicion_victimas vs muertes\n")
        condicion_1 = df[df["victims_condition"] == "With injured victims"]["deaths"]
        condicion_2 = df[df["victims_condition"] == "With dead victims"]["deaths"]

        if len(condicion_1) > 1 and len(condicion_2) > 1:
            resultado_ttest = stats.ttest_ind(condicion_1, condicion_2)
            f.write(f"Estadístico t: {resultado_ttest.statistic}\n")
            f.write(f"Valor p: {resultado_ttest.pvalue}\n\n")
        else:
            f.write(
                "No se puede realizar T-test: No hay suficientes datos en las condiciones\n\n"
            )

    return archivo_salida
