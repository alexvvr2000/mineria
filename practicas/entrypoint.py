from pathlib import Path

from codigo.practica_2 import obtener_dataframe, obtener_histograma
from codigo.practica_3 import lista_visualizaciones

FOLDERS_PRACTICAS = [Path("/output/Practica2"), Path("/output/Practica3")]

for practica in FOLDERS_PRACTICAS:
    practica.mkdir(
        parents=True,
    )


P2_resumen = FOLDERS_PRACTICAS[0] / "Resumen.csv"
P2_resumen.touch()

DATOS = Path("/datos.csv")
ArchivoDatos = obtener_dataframe(DATOS)

folder_histograma = obtener_histograma(FOLDERS_PRACTICAS[0], ArchivoDatos)
descripcion = ArchivoDatos.describe()
descripcion.to_csv(P2_resumen)
print("Creada practica 2")

archivos = lista_visualizaciones(ArchivoDatos, FOLDERS_PRACTICAS[1])
print("Creada practica 3")
