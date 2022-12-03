import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import plotly.graph_objects as go
import squarify
import plotly.express as px
from PIL import Image
from collections import Counter
from pywaffle import Waffle

#Page
st.set_page_config(layout="wide")

st.title("Proyecto de Internalización")

expansión = st.expander("Acerca")
expansión.markdown("""
* **Autor:** Luis Camilo Angel Sesma
* **Matrícula:** A01253231
* **Créditos:** freeCodeCamp.org YT
""")


col1 = st.sidebar
col2, col3, col4 =st.columns((5,1,4))

#Archivo BD
@st.cache
def read_data():
       bd=pd.read_excel("Prueba-Stream.xlsx")
       return bd

db=read_data()

#SideBar
#Imagen
imagen=Image.open("A01253231_IIS_CamiloAngel2.jpg")
col1.image(imagen, caption="-=Autor=-")
col1.header("Parámetros de búsqueda")

check = col1.checkbox("Selección de Datos")
if check:
       unique_escuela = sorted(db["Escuela"].unique())
       selección_escuela = col1.multiselect("Escuela", unique_escuela, unique_escuela)
db2=db[(db["Escuela"].isin(selección_escuela))]

#Selección de paises
sorted_país = sorted(db2["País"].unique())
selección_país = col1.multiselect("Paises", sorted_país, sorted_país)

db_selección_paises = db2[(db2["País"].isin(selección_país))]

#Nivel Academico
Niveles=db_selección_paises["Nivel"].unique()
Nivel = col1.multiselect("Nivel Academico", Niveles, Niveles)

db_selección_nivel = db_selección_paises[(db_selección_paises["Nivel"].isin(Nivel))]

#Puntuaje de Asignación
#
#col 2
#col2.subheader("Dimensión de la **Base de Datos**")
#col2.write("**Dimensión de los datos:** " + str(db_selección_nivel.shape[0]) + " filas y " + str(db_selección_nivel.shape[1]) + " columnas")
#col2.dataframe(db_selección_nivel[["Matrícula","PuntajeAsignación","Nivel","País","Escuela"]])

#col2
col2.markdown("<h1 style='text-align: center; color: black; font-size: 2.2rem;'>Representación mundial</h1>", unsafe_allow_html=True)

#col4
col4.markdown("<h1 style='text-align: center; color: black; font-size: 2.2rem;'>Alumnos por Nivel</h1>", unsafe_allow_html=True)
#Gráfica de Barras
Valores=db_selección_nivel["Nivel"].value_counts().tolist()
N_Nivel=db_selección_nivel["Nivel"].value_counts().keys().tolist()
#DataFrame 1
db3=pd.DataFrame()
db3["Nivel"]=N_Nivel
db3["Total"]=Valores
fig = px.bar(db3, x=db3["Nivel"], y=db3["Total"], hover_name=db3["Nivel"], color=db3["Total"], color_continuous_scale="Oranges")
col4.plotly_chart(fig)

#Mapa Mundial
x=db_selección_nivel["País"].value_counts().tolist()
y=db_selección_nivel["País"].value_counts().keys().tolist()
z=db_selección_nivel["iso_alpha"].value_counts().keys().tolist()
# DataFrame 2
db4=pd.DataFrame()
db4["País"]=y
db4["iso_alpha"]=z
db4["Total"]=x
#Graph
fig3 = px.choropleth(db4, locations=db4["iso_alpha"], color=db4["Total"], hover_name=db4["País"], color_continuous_scale="Oranges", range_color=[1,1600])
col2.plotly_chart(fig3)

#col2
col3.markdown("<h1 style='text-align: center; color: black; font-size: 2.2rem;'>Totales</h1>", unsafe_allow_html=True)

x=0
for i in db_selección_nivel["Intercambio"]:
       if i==1:
              x+=1
col3.write("<h1 style='text-align: center; color: black; font-size: 1rem;'>#de INT</h1>", unsafe_allow_html=True)
col3.markdown(f"<h1 style='text-align: center; color: Orange; font-size: 3rem;'>{x}</h1>", unsafe_allow_html=True)

y=0
for i in db_selección_nivel["Intercambio"]:
       if i==0:
              y+=1
col3.write("<h1 style='text-align: center; color: black; font-size: 1rem;'>#de No INT</h1>", unsafe_allow_html=True)
col3.markdown(f"<h1 style='text-align: center; color: Orange; font-size: 3rem;'>{y}</h1>", unsafe_allow_html=True)
col3.markdown("<h1 style='text-align: center; color: Black; font-size: 1rem;'>Porcentaje Total</h1>", unsafe_allow_html=True)
col3.markdown(f"<h1 style='text-align: center; color: Orange; font-size: 3rem;'>{round((x/(x+y)*100),2)}% </h1>", unsafe_allow_html=True)

#Tree Map
col4.markdown("<h1 style='text-align: center; color: black; font-size: 2.2rem;'>Distribución de Alumnos por Escuela</h1>", unsafe_allow_html=True)
#Nuevo
TreeMap=db_selección_nivel
TreeMap["Escuela"].unique().tolist()
Tree=TreeMap["Escuela"].value_counts().tolist()
col4.markdown(f"<h1 style='text-align: center; color: orange; font-size: 1.5rem;'>La Escuela de {TreeMap.Escuela.unique().tolist()[0]} es la mayor</h1>", unsafe_allow_html=True)
df_TreeMap=pd.DataFrame()
df_TreeMap["Escuela"]=TreeMap["Escuela"].unique().tolist()
df_TreeMap["Total"]=Tree
df_TreeMap["Alumnos"]="Alumnos"
fig2= px.treemap(df_TreeMap, path=["Alumnos",'Escuela'], values='Total',
                  color='Total', hover_data=['Escuela'],
                  color_continuous_scale='Oranges')
col4.plotly_chart(fig2)

#db_selección_nivel["Alumnos"]="Alumnos"
#fig2= px.treemap(db_selección_nivel, path=["Alumnos","Escuela","Nivel","País"],
#              color="Escuela", hover_data=["Nivel"],
#              color_continuous_scale="Oranges")
#col4.plotly_chart(fig2)

#Gráfica Waffle
col2.markdown("<h1 style='text-align: center; color: black; font-size: 2.2rem;'>(%) Primera Opción</h1>", unsafe_allow_html=True)
#Primera Opción
PrimeraOpción=db_selección_nivel["Primera Opción"]==db_selección_nivel["Opción Asignada"]
Verdaderos = Counter(PrimeraOpción)
Proporción=(Verdaderos[1])/(Verdaderos[1]+Verdaderos[0])*100
col2.write(f"<h1 style='text-align: center; color: orange; font-size: 1.5rem;'>El % de alumnos en su primera opción es: {round(Proporción,2)} % </h1>", unsafe_allow_html=True)
col2.write(f"<h1 style='text-align: center; color: orange; font-size: 1.2rem;'>Siendo {Verdaderos[1]} que Sí  y {Verdaderos[0]} que No</h1>", unsafe_allow_html=True)
datos={"Verdaderos":99, "Falsos": 1}
fig4 = plt.figure(
    FigureClass=Waffle, 
    rows=5,
    columns=20, 
    values=datos, 
    colors=("#FAE5D3", "#17202A"),
    labels=["{0} ({1}%)".format(k, v) for k, v in datos.items()],
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.4), 'ncol': len(datos), 'framealpha': 0}
)
fig4.gca().set_facecolor('#D68910')
fig4.set_facecolor('#D68910')
col2.pyplot(fig4)

#Avión
imagen2=Image.open("Avion.png")
col3.image(imagen2)



