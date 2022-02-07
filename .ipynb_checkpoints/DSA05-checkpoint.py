import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


DATA_URL = './Employees_DSA05.csv'
employees = pd.DataFrame()


# Carga de DF con un limite nrows
@st.cache
def load_data(nrows=False):
    if nrows:
        employees = pd.read_csv(DATA_URL, nrows=nrows)
    else:
        employees = pd.read_csv(DATA_URL)
    return employees

@st.cache
def filter_by_criteria(employees, keyword):
    filtered_data_filme = employees[(employees['Employee_ID'].str.contains(keyword)) |
                               (employees['Hometown'].str.contains(keyword)) |
                               (employees['Unit'].str.contains(keyword))
                              ]
    return filtered_data_filme


@st.cache
def filter_education_level(employees, filter_by_education_level):
    employees = employees[(employees['Education_Level'] == int(filter_by_education_level))]
    return employees

@st.cache
def filter_by_cities(employees, filter_by_cities_keyword):
    employees = employees[(employees['Hometown'] == filter_by_cities_keyword)]
    return employees

@st.cache
def filter_by_unit(employees, filter_by_unit):
    employees = employees[(employees['Unit'] == filter_by_unit)]
    return employees



st.title("Análisis de deserción de empleados")
st.markdown("En los retos de los módulos previos, trabajaste con los datos provistos en el Hackathon HackerEarth 2020, tomando como hipótesis que esta información resultará explicativa del fenómeno de deserción laboral que tanto afecta en la actualidad a las empresas y organizaciones.")

st.markdown("Ya has completado algunas observaciones elementales y sintetizado dicha información mediante técnicas de filtrado y agrupación. Tu trabajo en esta fase consiste en complementar el análisis de datos con la representación en un dashboard usando Streamlit de manera eficiente y atractiva para un usuario final.")

# Definicion de filtros y cargas del DF
sidebar = st.sidebar

sidebar.title("Filtros")
show_full_list_employee = sidebar.checkbox('Ver toda lista de empleados')

if(show_full_list_employee):
    employees = load_data()
else:
    employees = load_data(500)

keyword = sidebar.text_input('Busqueda', placeholder="Buscar por Employee_ID, Hometown o Unit",)
filter_by_education_level = sidebar.selectbox('Nivel educativo', employees['Education_Level'].unique())

filter_by_cities_keyword = sidebar.selectbox('Por ciudad', employees['Hometown'].unique())


filter_by_unit_keyword = sidebar.selectbox('Por unidad', employees['Unit'].unique())

filters_clicked = sidebar.button("Aplicar filtros")

if filters_clicked:
    if keyword:
        employees = filter_by_criteria(employees, keyword)
        

    if filter_by_education_level:
        employees = filter_education_level(employees, filter_by_education_level)
   

    if filter_by_cities_keyword:
        employees = filter_by_cities(employees, filter_by_cities_keyword)
    
    if filter_by_unit_keyword:
        employees = filter_by_unit(employees, filter_by_unit_keyword )
    
st.dataframe(employees)   
st.text(f"Empleados: ({employees.shape[0]})")


st.markdown("### Comportamiento de varoles nulos")
st.text(employees.isna().sum())


st.markdown("### Histograma de empleados agrupados por edad")
employees_cleaned = employees['Age'].dropna()
hist_values = np.histogram(employees_cleaned, bins=int(employees_cleaned.max()),
                           range=(0,employees_cleaned.max()),   )[0]
st.bar_chart(hist_values)
 
st.markdown("### Grafica de frecuencias por unidad")

freq_unit = employees.groupby('Unit').count()
st.bar_chart(freq_unit['Employee_ID'])
 
st.markdown("### Analisis de ciudad con mayor indice de deserción")

freq_unit = employees.groupby('Hometown').count()
st.bar_chart(freq_unit['Attrition_rate'])
 
st.markdown("### Edad y Tasa de deserción")

freq_unit = employees.groupby('Age').count()
st.bar_chart(freq_unit['Attrition_rate'])
 
 
corr = employees.corr()
     

  
st.markdown("### Relacion entre Tiempo de servicio y deserción")
st.text("Como se puede observar, no existe una relacion directa entre tiempo de servicio y deserción")
#Create numpy array for the visualisation
x = employees['Time_of_service']
y = employees['Attrition_rate']
 
fig = plt.figure(figsize=(10, 4))
plt.scatter(x, y)
    
st.pyplot(fig)

