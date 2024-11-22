from pathlib import Path

from codigo.practica_2 import obtener_dataframe, obtener_histograma

FOLDER_PRACTICA2 = Path("/output/Practica2")
FOLDER_PRACTICA2.mkdir(
    parents=True,
)
P2_resumen = FOLDER_PRACTICA2 / "Resumen.csv"
P2_resumen.touch()

DATOS = Path("/datos.csv")
ArchivoDatos = obtener_dataframe(DATOS)

folder_histograma = obtener_histograma(FOLDER_PRACTICA2, ArchivoDatos)
descripcion = ArchivoDatos.describe()
descripcion.to_csv(P2_resumen)
print("Creada practica 2")
