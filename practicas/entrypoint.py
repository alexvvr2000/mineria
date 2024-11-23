from pathlib import Path

from codigo.practica_2 import obtener_dataframe, obtener_histograma
from codigo.practica_3 import lista_visualizaciones
from codigo.practica_4 import ejecutar_anova_ttest
from codigo.practica_5 import generar_modelo_lineal
from codigo.practica_6 import generar_modelo_knn
from codigo.practica_7 import generar_modelo_kmeans
from codigo.practica_8 import generar_modelo_lineal_serie_temporal
from codigo.practica_9 import generar_nube_de_palabras

FOLDERS_PRACTICAS: tuple[Path, ...] = (
    Path("/output/Practica2"),
    Path("/output/Practica3"),
    Path("/output/Practica4"),
    Path("/output/Practica5"),
    Path("/output/Practica6"),
    Path("/output/Practica7"),
    Path("/output/Practica8"),
    Path("/output/Practica9"),
)

for practica in FOLDERS_PRACTICAS:
    practica.mkdir(parents=True, exist_ok=True)


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

ejecutar_anova_ttest(ArchivoDatos, FOLDERS_PRACTICAS[2])
print("Creada practica 4")

generar_modelo_lineal(ArchivoDatos, FOLDERS_PRACTICAS[3])
print("Creada practica 5")

generar_modelo_knn(ArchivoDatos, FOLDERS_PRACTICAS[4])
print("Creada practica 6")

generar_modelo_kmeans(ArchivoDatos, FOLDERS_PRACTICAS[5])
print("Creada practica 7")

generar_modelo_lineal_serie_temporal(ArchivoDatos, FOLDERS_PRACTICAS[6])
print("Creada practica 8")

generar_nube_de_palabras(FOLDERS_PRACTICAS[7], ArchivoDatos)
print("Creada practica 9")
