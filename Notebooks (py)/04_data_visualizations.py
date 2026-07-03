import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl
import os

'''
REPRESENTACIONES A HACER
1. 
'''

#IMPORTACIÓN DE NUESTRO DATAFRAME
pd.set_option('display.max_columns', None)
file1 = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/03_merge_dataframes.csv"
df_final = pd.read_csv(file1, index_col = 0)
print(df_final.head(10))

#VISUALIZACIONES DE LOS DATOS
#1. Estudio de la distribución de los datos: Estudio de cómo se distribuyen el total de los clientes en función de los grupos categóricos
#que hemos establecido para las diferentes variables.
    #Distribución por grupos de edad (uso el mismo bloque de código para el resto de pie charts, así que lo explico aquí únicamente)
df_pie1 = df_final['Age group'].value_counts().reset_index() #Conteo de los valores correspondientes a cada categoría
df_pie1.columns = ['Age group', 'Count'] #Renombro la columna 'count' para igualar el formato que he aplicado al resto de columnas
df_pie1.sort_values(by = 'Count', ascending = False, inplace = True) #Ordeno las categorías, en orden descendente, según el número de valores
fig1 = plt.figure(figsize = (10,10)) #Defino el tamaño del 'lienzo' de mi figura
plt.title('Distribution of clients by age group',
          fontsize = 40) #Título, y su correspondiente formato, de mi gráfico de sectores
sns.set_style('whitegrid') #Defino el estilo del gráfico
explode1 = [0.05, 0, 0, 0] #Lista 'explode' para aplicar al parámetro explode en mi gráfico de sectores. Con esto, conseguimos que un sector
#sobresalga ligeramente por encima del resto
plt.pie(data = df_pie1, # Dataframe del que extraemos los datos
        x = 'Count', #Los valores que van a determinar el tamaño de los sectores
        labels = 'Age group', #Etiquetas de cada sector
        colors = sns.color_palette('pastel'), #Paleta de colores
        textprops = {
            'fontsize': 30 #Propiedades del texto en el gráfico -> tamaño de la fuente
            },
        autopct = '%1.2f%%', #Muestra los porcentajes en cada sector, con dos números decimales
        explode = explode1, #Nuestros parámetros de 'explode', definidos previamente
        startangle = 90, #El primer sector empieza en un ángulo exacto de 90 grados (aporta más consistencia en la estética)
        pctdistance = 0.75, #Distancia entre el centro del gráfico a los valores de porcentaje de cada sector
        labeldistance = 1.1 #Distancia entre las etiquetas y la circunferencia
        )
plt.tight_layout() #Este comando ajusta los espacios que hay entre figuras y elementos de figuras. No estoy seguro de si en este caso concreto
#aporta mucho, pero siempre lo añado por si acaso (a no ser que note que empeora el formato en vez de mejorarlo)
plt.show() #Mostramos nuestro gráfico

    #Distribución por grupos de trabajo
df_pie2 = df_final['Job group'].value_counts().reset_index()
df_pie2.columns = ['Job group', 'Count']
df_pie2.sort_values(by = 'Count', ascending = False, inplace = True)
fig2, ax2 = plt.subplots(figsize=(10, 10)) #En este caso, defino un 'fig, ax' ya que voy a realizar otras modificaciones en esta figura,
#sobre todo por cuestiones de legibilidad; por ejemplo, voy a añadir y personalizar una leyenda
plt.title('Distribution of clients by job group',
          fontsize = 30)
sns.set_style('whitegrid')
explode2 = [0.05, 0, 0, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return '<1%'
    else:
        return np.round(pct,2)
plt.pie(data = df_pie2,
        x = 'Count',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 12
            },
        autopct = autopct_format,
        explode = explode2,
        startangle = 90,
        pctdistance = 0.95,
        )
ax2.legend( #Para este pie chart en concreto, he preferido añadir una leyenda en vez de incluir los valores de los sectores en el gráfico,
    #ya que al haber varios sectores de pequeño tamaño juntos, dificultaba mucho su legibilidad
    df_pie2['Job group'], #Columna de la que sacamos las etiquetas de los valores
    title='Job group', #Título de la leyenda
    title_fontsize = 'xx-large', #Tamaño del título de la leyenda
    loc='upper right', #Localización de la caja de la leyenda
    fontsize='x-large' #Tamaño de los elementos de la leyenda
)
plt.tight_layout()
plt.show()

#Distribución por trabajos (categoría: Employee)
df_pie3 = df_final[df_final['Job group']=='Employee']
df_pie3 = df_pie3['Job'].value_counts().reset_index()
df_pie3.columns = ['Job', 'Count']
df_pie3.sort_values(by = 'Count', ascending = False, inplace = True)
print(df_pie3)
fig3, ax3 = plt.subplots(figsize=(10, 10))
plt.title('Distribution of employees by job',
          fontsize = 30)
sns.set_style('whitegrid')
explode3 = [0.05, 0, 0, 0, 0, 0, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return '<1%'
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie3,
        x = 'Count',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 13
            },
        autopct = autopct_format,
        explode = explode3,
        startangle = 90,
        pctdistance = 0.92,
        )

ax3.legend(
    df_pie3['Job'],
    title='Job (Employees)',
    title_fontsize = 'xx-large',
    loc='upper right',
    fontsize='x-large'
)
plt.tight_layout()
plt.show()

    #Distribución por grupos de educación recibida
df_pie4 = df_final['Educational group'].value_counts().reset_index()
df_pie4.columns = ['Educational group', 'Count']
df_pie4.sort_values(by = 'Count', ascending = False, inplace = True)
fig4, ax4 = plt.subplots(figsize=(10, 10))
plt.title('Distribution of clients by educational group',
          fontsize = 30)
sns.set_style('whitegrid')
explode4 = [0.05, 0, 0, 0, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return '<1%'
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie4,
        x = 'Count',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 16
            },
        autopct = autopct_format,
        explode = explode4,
        startangle = 90,
        pctdistance = 0.91
        )
ax4.legend(
    df_pie4['Educational group'],
    title='Educational group',
    title_fontsize = 'xx-large',
    loc='upper right',
    fontsize='x-large'
)
plt.tight_layout()
plt.show()

    #Distribución por estado civil
df_pie5 = df_final['Marital status'].value_counts().reset_index()
df_pie5.columns = ['Marital status', 'Count']
df_pie5.sort_values(by = 'Count', ascending = False, inplace = True)
fig5 = plt.figure(figsize=(10, 10))
plt.title('Distribution of clients by marital status',
          fontsize = 30)
sns.set_style('whitegrid')
explode5 = [0.05, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return '<1%'
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie5,
        x = 'Count',
        labels = 'Marital status', #Volvemos a usar las labels ya que en este caso sí que se leen bien cuando se sitúan en la gráfica
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 25
            },
        autopct = autopct_format,
        explode = explode5,
        startangle = 90,
        pctdistance = 0.70,
        labeldistance = 1.1
        )
plt.tight_layout()
plt.show()

    #Distribución de clientes en función de si tienen o no una hipoteca
df_pie6 = df_final['Mortgage (Yes/No)'].value_counts().reset_index()
df_pie6.columns = ['Mortgage', 'Count']
df_pie6.sort_values(by = 'Count', ascending = False, inplace = True)
fig6 = plt.figure(figsize=(10, 10))
plt.title('Do the clients have a mortgage loan?',
          fontsize = 30)
sns.set_style('whitegrid')
explode6 = [0.05, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return '<1%'
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie6,
        x = 'Count',
        labels = 'Mortgage',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 15
            },
        autopct = autopct_format,
        explode = explode6,
        startangle = 90,
        pctdistance = 0.87,
        labeldistance = 1.1
        )
plt.tight_layout()
plt.show()

    #Distribución de clientes en función de si tienen o no algún otro préstamo
df_pie7 = df_final['Other loans (Yes/No)'].value_counts().reset_index()
df_pie7.columns = ['Other loans', 'Count']
df_pie7.sort_values(by = 'Count', ascending = False, inplace = True)
fig7 = plt.figure(figsize=(10, 10))
plt.title('Do the clients have another kind of loan?',
          fontsize = 30)
sns.set_style('whitegrid')
explode7 = [0.05, 0]
def autopct_format(pct):
    if pct < 1:
        return '<1%'
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie7,
        x = 'Count',
        labels = 'Other loans',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 25
            },
        autopct = autopct_format,
        explode = explode7,
        startangle = 90,
        pctdistance = 0.82,
        labeldistance = 1.1
        )
plt.tight_layout()
plt.show()

    #Distribución de clientes en función del resultado obtenido en la última campaña de marketing
df_pie8 = df_final['Prev. marketing campaign'].value_counts().reset_index()
df_pie8.columns = ['Previous campaign', 'Count']
df_pie8.sort_values(by = 'Count', ascending = False, inplace = True)
fig8 = plt.figure(figsize=(10, 10))
plt.title('What was the result of the previous marketing campaign?',
          fontsize = 30)
sns.set_style('whitegrid')
explode8 = [0.05, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return '<1%'
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie8,
        x = 'Count',
        labels = 'Previous campaign',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 18
            },
        autopct = autopct_format,
        explode = explode8,
        startangle = 90,
        pctdistance = 0.87,
        labeldistance = 1.1
        )
plt.tight_layout()
plt.show()


    # Distribución de clientes en función de las veces que se les contactó antes de la campaña
#En este caso, la alta diferencia entre los valores de los diferentes datos nos dificulta mucho la creación de un gráfico de sectores,
#ya que varios sectores ni siquiera se apreciaban correctamente. Debido a ello, he decidido representarlo como un gráfico de barras
df_bar9 = df_final['#Contacts before campaign'].value_counts().reset_index()
df_bar9.columns = ['Contacts before', 'Count']
df_bar9.sort_values(by = 'Count', ascending = False, inplace = True)
fig9, ax9 = plt.subplots(figsize=(10, 10))
bar9 = sns.barplot( #En vez del método plt.pie, utilizamos sns.barplot, indicando los datos de manera similar
            data = df_bar9,
            x = 'Contacts before',
            y = 'Count',
)
plt.title('How many calls did the client receive befor the campaign',
          fontsize = 30)
for container in bar9.containers:
    #En este bucle for, hacemos lo siguiente: las barras creadas para el objeto bar9 (nuestra gráfica de barras) se catalogan como containers
    #en Python, y se puede iterar a través de ellos. Por lo tanto, iteramos a través de dichas barras para que, en cada una, le podamos añadir
    # el valor correspondiente; de esta manera, vemos el valor absoluto de los clientes que han recibido los diferentes números de llamada
    bar9.bar_label(bar9.containers[bar9.containers.index(container)], padding = 3) #padding es el espacio entre elementos, en este caso,
    #entre la barra y su valor correspondiente, que estará colocado encima de manera predeterminada
plt.xticks(fontsize = 20,
           rotation=45)
plt.yticks(fontsize = 20)
plt.ylabel('Clients contacted before the campaign',
           fontsize = 25,
           labelpad = 30)
plt.xlabel('Number of contacts before the campaign',
           fontsize = 25,
           labelpad = 30)
plt.minorticks_on()
plt.show()

    #Distribución de clientes en función de cuánto duró la última llamada realizada con ellos
df_pie10 = df_final['Last call (range)'].value_counts().reset_index()
df_pie10.columns = ['Last call (range)', 'Count']
df_pie10.sort_values(by = 'Count', ascending = False, inplace = True)
fig10, ax10 = plt.subplots(figsize=(10, 10))

plt.title('How much did the last call with the client last?',
          fontsize = 30)
sns.set_style('whitegrid')
explode10 = [0.05, 0, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie10,
        x = 'Count',
        # labels = 'Last call (range)',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 16
            },
        autopct = autopct_format,
        explode = explode10,
        startangle = 90,
        pctdistance = 0.85,
        # labeldistance = 1.1
        )
ax10.legend(
    df_pie10['Last call (range)'],
    title='Last call duration',
    title_fontsize = 'xx-large',
    loc='upper right',
    fontsize='x-large',
    ncol = 2 #Definimos el número de columnas que queremos que tenga la leyenda, para que no se superponga con el gráfico
)
plt.tight_layout()
plt.show()

    #Distribución de clientes en función de cuántos días han transcurrido desde la última llamada con el cliente
df_pie11 = df_final['Days from last call (range)'].value_counts().reset_index()
df_pie11.columns = ['Days from last call (range)', 'Count']
df_pie11.sort_values(by = 'Count', ascending = False, inplace = True)
fig11 = plt.figure(figsize=(10, 10))

plt.title('Days elapsed from the last call with the client',
          fontsize = 30)
sns.set_style('whitegrid')
explode11 = [0.05, 0]
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie11,
        x = 'Count',
        labels = 'Days from last call (range)',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 18
            },
        autopct = autopct_format,
        explode = explode11,
        startangle = 90,
        pctdistance = 0.88,
        labeldistance = 1.1
        )
plt.tight_layout()
plt.show()

    #Distribución de clientes en función de los contactos realizados con el cliente durante la campaña de marketing
df_pie12 = df_final['Contacts during campaign (range)'].value_counts().reset_index()
df_pie12.columns = ['Contacts during', 'Count']
df_pie12.sort_values(by = 'Count', ascending = False, inplace = True)
fig12, ax12 = plt.subplots(figsize=(10, 10))

plt.title('Number of contacts with the client during the campaign',
          fontsize = 30)
sns.set_style('whitegrid')
explode12 = [0.05, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie12,
        x = 'Count',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 16
            },
        autopct = autopct_format,
        explode = explode12,
        startangle = 90,
        pctdistance = 0.90,
        )
ax12.legend(
    df_pie12['Contacts during'],
    title='Contacts during campaign',
    title_fontsize = 'xx-large',
    loc='upper right',
    fontsize='x-large',
)
plt.tight_layout()
plt.show()

    #Distribución de clientes en función del año en el que fueron contactados
df_pie13 = df_final['Contact date (year)'].value_counts().reset_index()
df_pie13.columns = ['Contact year', 'Count']
df_pie13.sort_values(by = 'Count', ascending = False, inplace = True)
fig13, ax13 = plt.subplots(figsize=(10, 10))

plt.title('Year when the client was contacted',
          fontsize = 30)
sns.set_style('whitegrid')
explode13 = [0.05, 0, 0, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie13,
        x = 'Count',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 24
            },
        autopct = autopct_format,
        explode = explode13,
        startangle = 90,
        pctdistance = 0.70,
        )
ax13.legend(
    df_pie13['Contact year'],
    title='Contact year',
    title_fontsize = 'xx-large',
    loc='upper right',
    fontsize='x-large',
    ncol = 2
)
plt.tight_layout()
plt.show()

    #Distribución de clientes en función de si se han suscrito a nuestro producto/servicio o no (es decir, en función del resultado
    #de la variable objetivo
df_pie14 = df_final['Objective variable'].value_counts().reset_index()
df_pie14.columns = ['Objective variable', 'Count']
df_pie14.sort_values(by = 'Count', ascending = False, inplace = True)
fig14 = plt.figure(figsize=(10, 10))

plt.title('Did the client subscribe to our product/service?',
          fontsize = 30)
sns.set_style('whitegrid')
explode14 = [0.05, 0]
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie14,
        x = 'Count',
        labels = 'Objective variable',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 24
            },
        autopct = autopct_format,
        explode = explode14,
        startangle = 90,
        pctdistance = 0.70,
        labeldistance = 1.1
        )
plt.tight_layout()
plt.show()

    #Distribución de clientes en función del salario percibido anualmente (organizado en rangos)
df_pie15 = df_final['Annual income (range)'].value_counts().reset_index()
df_pie15.columns = ['Income', 'Count']
df_pie15.sort_values(by = 'Count', ascending = False, inplace = True)
fig15 = plt.figure(figsize=(10, 10))

plt.title('Range of Annual income of our clients',
          fontsize = 30)
sns.set_style('whitegrid')
explode15 = [0.05, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie15,
        x = 'Count',
        labels = 'Income',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 18
            },
        autopct = autopct_format,
        explode = explode15,
        startangle = 90,
        pctdistance = 0.70,
        labeldistance = 1.1
        )
plt.tight_layout()
plt.show()

    #Distribución de clientes en función del número de hijos que tienen en casa
df_pie16 = df_final['# Kids at home'].value_counts().reset_index()
df_pie16.columns = ['Kids', 'Count']
df_pie16.sort_values(by = 'Count', ascending = False, inplace = True)
fig16, ax16 = plt.subplots(figsize=(10, 10))

plt.title('Number of kids at home ',
          fontsize = 30)
sns.set_style('whitegrid')
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie16,
        x = 'Count',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 24
            },
        autopct = autopct_format,
        startangle = 90,
        pctdistance = 0.70
        )
ax16.legend(
    df_pie16['Kids'],
    title='Number of kids',
    title_fontsize = 'xx-large',
    loc='upper right',
    fontsize='x-large',
)
plt.tight_layout()
plt.show()

    #Distribución de clientes en función del número de hijos adolescentes que tienen en casa
df_pie17 = df_final['# Teens at home'].value_counts().reset_index()
df_pie17.columns = ['Teens', 'Count']
df_pie17.sort_values(by = 'Count', ascending = False, inplace = True)
fig17, ax17 = plt.subplots(figsize=(10, 10))

plt.title('Number of teens at home',
          fontsize = 30)
sns.set_style('whitegrid')
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie17,
        x = 'Count',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 24
            },
        autopct = autopct_format,
        startangle = 90,
        pctdistance = 0.70
        )
ax17.legend(
    df_pie17['Teens'],
    title='Number of teens at home',
    title_fontsize = 'xx-large',
    loc='upper right',
    fontsize='x-large',
)
plt.tight_layout()
plt.show()

    #Distribución de clientes en función de la frecuencia mensual de visita a nuestra página web
df_pie18 = df_final['Web visit freq. (per month)'].value_counts().reset_index()
df_pie18.columns = ['Frequency', 'Count']
df_pie18.sort_values(by = 'Count', ascending = False, inplace = True)
fig18 = plt.figure(figsize=(10, 10))

plt.title('Website visit frequency (per month)',
          fontsize = 30)
sns.set_style('whitegrid')
explode18 = [0.05, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie18,
        x = 'Count',
        labels = 'Frequency',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 24
            },
        autopct = autopct_format,
        explode = explode18,
        startangle = 90,
        pctdistance = 0.70,
        labeldistance = 1.1
        )
plt.tight_layout()
plt.show()

    #Distribución de clientes en función del año en que se registraron como clientes
df_pie19 = df_final['Register date (year)'].value_counts().reset_index()
df_pie19.columns = ['Year', 'Count']
df_pie19.sort_values(by = 'Count', ascending = False, inplace = True)
fig19, ax19 = plt.subplots(figsize=(10, 10))

plt.title('Year of client register',
          fontsize = 30)
sns.set_style('whitegrid')
explode19 = [0.05, 0, 0]
def autopct_format(pct):
    if pct < 1:
        return ''
    else:
        pct_rounded = str(np.round(pct,2))
        return f'{pct_rounded}%'
plt.pie(data = df_pie19,
        x = 'Count',
        # labels = 'Frequency',
        colors = sns.color_palette('pastel'),
        textprops = {
            'fontsize': 24
            },
        autopct = autopct_format,
        explode = explode19,
        startangle = 90,
        pctdistance = 0.70,
        # labeldistance = 1.1
        )
ax19.legend(
    df_pie19['Year'],
    title='Year',
    title_fontsize = 'xx-large',
    loc='upper right',
    fontsize='x-large'
)
plt.tight_layout()
plt.show()

#2. Relación de las diferentes variables con la variable objetivo: Una vez vistos los diferentes grupos en los que podemos dividir nuestro datos
#en función de las diferentes variables, podemos estudiar la distribución de nuestra variable objetivo en dichos grupos. Para ello, vamos a diseñar
#gráficas de barras apiladas:
# VARIABLE Age group: Estudiamos la distribución de Yes y No para nuestra variable objetivo (si el cliente ha contratado algún servicio/
# producto) en los diferentes grupos de edad. El funcionamiento será muy similar para el resto de variables, así que los pasos generales a
# seguir se explicarán en este primer caso. Usaremos barras apiladas con esta finalidad
fig1 = plt.figure(figsize=(10, 10))  # Definimos la figura, como hemos hecho en los casos anteriores
hist1 = sns.histplot(
    # Hacemos un histograma, ya que según la documentación de seaborn, esto nos va a permitir apilar barras de forma sencilla
    data=df_final,  # Definimos la fuente de nuestros datos, es decir, nuestro dataframe
    x='Age group',  # Definimos el eje X, en este caso, los diferentes grupos de edad en nuestra variable
    hue='Objective variable',
    # Definimos la variable a ser representada, en el caso de estas representaciones, será nuestra variable objetivo
    palette='pastel',  # Definimos la paleta de colores que queremos usar (únicamente con fines estéticos)
    multiple='fill',  # La opción que nos va a permitir apilar elementos, gracias a que elegimos el parámetro 'fill'
    stat='proportion',
    # Va a ajustar las barras para representarlas como valores relativos en escala de 1, de manera que la suma de las barras
    # apiladas sea siempre 1; a pesar de ello, indicaré el valor dentro de la barra en porcentaje, ya que me parece más intuitivo
    discrete=True,
    # Cuando este parámetro es True, le indicamos que la anchura de la barra es 1, y que por tanto la barra tiene que quedar
    # centrada con su valor correspondiente. Básicamente, le estamos indicando que nuestros valroes son discretos y no continuos
    shrink=.6  # Valor para definir la anchura relativa de la barra.
)
# Modificamos el título del gráfico y los título de los ejes, esta vez usando la nomenclatura de seaborn en vez de matplotlib (p. ej. usamos
# .set_title() en vez de .title()
hist1.set_ylabel('Proportion of clients', fontsize=30)
hist1.set_xlabel('Age group', fontsize=30)
hist1.set_title('Objective variable depending on age group', fontsize=40)
# Ahora procedemos a la creación de las etiquetas, siguiendo una metodología parecida a la usada para df_bar9 en el anterior apartado
for container in hist1.containers:  # Mismo razonamiento de antes. Tenemos una lista de 'containers', cada uno correspondiente con una barra, así que
    # lo podemos tratar como un iterable
    labels_list = []  # Creamos una lista vacía, donde incluiremos las etiquetas
    for bar in container:  # En ese caso, cada contenedor (barra), tendrá su vez dos elementos (barra apilada inferior y barra apilada superior). Por
        # tanto, podemos tratar a las barras (bar) a su vez como un iterable
        label = f'{np.round(bar.get_height() * 100, 2)}%'  # Definimos la etiqueta con .get_height para obtener la altura de la barra. Debido a
        # nuestro stat = 'proportion', estará en escala de 1, así que multiplicaremos el valor por 100 y le añadiremos un '%' al final
        labels_list.append(
            label)  # Añadimos el valor obtenido a nuestra lista, y volvemos a iterar. Con la indentación que hemos seguido, vamos a
        # tener una lista de dos valores para cada barra (cada una formada a su vez por dos barras)
    hist1.bar_label(container, labels=labels_list, label_type='center',
                    fontsize=30)  # Definimos nuestras etiqeutas, pasando la lista de etiquetas,
    # y ajustando los formatos correspondientes
# Por último, definimos los tamaños de los ticks de cada eje, y finalmente mostramos el gráfico.
plt.xticks(rotation=0, fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
plt.show()

# VARIABLE Job group: Estudiamos la distribución de Yes y No para nuestra variable objetivo.
fig2 = plt.figure(figsize=(10,10))
hist2 = sns.histplot(
    data = df_final,
    x = 'Job group',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .6
)
hist2.set_ylabel('Proportion of clients', fontsize = 30)
hist2.set_xlabel('Job group', fontsize = 30)
hist2.set_title('Objective variable depending on job group', fontsize = 40)
for container in hist2.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist2.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Job (Employee): Estudiamos la distribución de Yes y No para los diferentes tipos de trabajadores por cuenta ajena.
fig3 = plt.figure(figsize=(10,10))
hist3 = sns.histplot(
    data = df_final,
    x = 'Job',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist3.set_ylabel('Proportion of clients', fontsize = 30)
hist3.set_xlabel('Job (employees)', fontsize = 30)
hist3.set_title('Objective variable depending on job (employees)', fontsize = 40)
for container in hist3.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist3.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 20)
plt.xticks(rotation = 45, fontsize = 15)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Educational group: Estudiamos la distribución de Yes y No para los grupos de clientes con diferentes formación académica.
fig4 = plt.figure(figsize=(10,10))
hist4 = sns.histplot(
    data = df_final,
    x = 'Educational group',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist4.set_ylabel('Proportion of clients', fontsize = 30)
hist4.set_xlabel('Educational group', fontsize = 30)
hist4.set_title('Objective variable depending on education', fontsize = 40)
for container in hist4.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist4.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Marital status: Estudiamos la distribución de Yes y No para los grupos de clientes en función de su estado civil.
fig5 = plt.figure(figsize=(10,10))
hist5 = sns.histplot(
    data = df_final,
    x = 'Marital status',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist5.set_ylabel('Proportion of clients', fontsize = 30)
hist5.set_xlabel('Marital status', fontsize = 30)
hist5.set_title('Objective variable depending on marital status', fontsize = 40)
for container in hist5.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist5.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Mortgage: Estudiamos la distribución de Yes y No en función de si los clientes tienen o no una hipoteca.
fig6 = plt.figure(figsize=(10,10))
hist6 = sns.histplot(
    data = df_final,
    x = 'Mortgage (Yes/No)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist6.set_ylabel('Proportion of clients', fontsize = 30)
hist6.set_xlabel('Does the client have a mortage loan?', fontsize = 30)
hist6.set_title('Objective variable depending on having a mortgage loan', fontsize = 40)
for container in hist6.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist6.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Other loans: Estudiamos la distribución de Yes y No en función de si los clientes tienen o no algún otro préstamo.
fig7 = plt.figure(figsize=(10,10))
hist7 = sns.histplot(
    data = df_final,
    x = 'Other loans (Yes/No)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist7.set_ylabel('Proportion of clients', fontsize = 30)
hist7.set_xlabel('Does the client have other loans?', fontsize = 30)
hist7.set_title('Objective variable depending on having other loans', fontsize = 40)
for container in hist7.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist7.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Prev. marketing campaign: Estudiamos la distribución de Yes y No en función del resultado en la campaña de marketing previa
fig8 = plt.figure(figsize=(10,10))
hist8 = sns.histplot(
    data = df_final,
    x = 'Prev. marketing campaign',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist8.set_ylabel('Proportion of clients', fontsize = 30)
hist8.set_xlabel('Result of previous marketing campaign', fontsize = 30)
hist8.set_title('Objective variable depending on the result of previous marketing campaign', fontsize = 35)
for container in hist8.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist8.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE #Contacts before campaign: Estudiamos la distribución de Yes y No en función del nº de contactos con el cliente antes de la campaña.
fig9 = plt.figure(figsize=(10,10))
hist9 = sns.histplot(
    data = df_final,
    x = '#Contacts before campaign',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist9.set_ylabel('Proportion of clients', fontsize = 30)
hist9.set_xlabel('#Contacts before the marketing campaign', fontsize = 30)
hist9.set_title('Objective variable depending on the contacts with the client before campaign', fontsize = 35)
for container in hist9.containers:
    labels_list = []
    for bar in container:
        height_bar = bar.get_height() * 100
        if height_bar == 0: #Añadimos un pequeño condicional 'if' para no incluir el porcentaje cuando éste sea igual a 0,
            #ya que no tiene espacio físico en el gráfico, y no aporta información, ya que ya tenemos la etiqueta del 100%
            label = ''
        else:
            label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist9.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Last call (range): Estudiamos la distribución de Yes y No en función de cuánto duró la última llamada con el cliente.
fig10 = plt.figure(figsize=(10,10))
hist10 = sns.histplot(
    data = df_final,
    x = 'Last call (range)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist10.set_ylabel('Proportion of clients', fontsize = 30)
hist10.set_xlabel('Duration of the last call', fontsize = 30)
hist10.set_title('Objective variable depending on the duration of the last call with the client', fontsize = 35)
for container in hist10.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist10.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 27)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Days from last call (range): Estudiamos la distribución de Yes y No en función de cuántos días hace da la última llamada
#con el cliente.
fig11 = plt.figure(figsize=(10,10))
hist11 = sns.histplot(
    data = df_final,
    x = 'Days from last call (range)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist11.set_ylabel('Proportion of clients', fontsize = 30)
hist11.set_xlabel('Days from the last call', fontsize = 30)
hist11.set_title('Objective variable depending on the days elapsed from the last call', fontsize = 35)
for container in hist11.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist11.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 35)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Contacts during campaign (range): Estudiamos la distribución de Yes y No en función del número de contactos con el cliente
#durante la campañaa de marketing
#con el cliente.
fig12 = plt.figure(figsize=(10,10))
hist12 = sns.histplot(
    data = df_final,
    x = 'Contacts during campaign (range)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist12.set_ylabel('Proportion of clients', fontsize = 30)
hist12.set_xlabel('# Contacts during the campaign', fontsize = 30)
hist12.set_title('Objective variable depending on the number of contacts during the campaign', fontsize = 32)
for container in hist12.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist12.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 22)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Contact date (year): Estudiamos la distribución de Yes y No en función del año en que se contactó con el cliente
#con el cliente.
fig13 = plt.figure(figsize=(10,10))
hist13 = sns.histplot(
    data = df_final,
    x = 'Contact date (year)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist13.set_ylabel('Proportion of clients', fontsize = 30)
hist13.set_xlabel('Contact year', fontsize = 30)
hist13.set_title('Objective variable depending on the year the client was contacted', fontsize = 35)
for container in hist13.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist13.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 28)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE IPC: Estudiamos la distribución de Yes y No en función del valor del IPC
fig14 = plt.figure(figsize=(10,10))
hist14 = sns.histplot(
    data = df_final,
    x = 'IPC (range)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist14.set_ylabel('Proportion of clients', fontsize = 30)
hist14.set_xlabel('IPC value', fontsize = 30)
hist14.set_title('Objective variable depending on the IPC value', fontsize = 35)
for container in hist14.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist14.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Confidence level (range): Estudiamos la distribución de Yes y No en función del valor de la confianza del consumidor
fig15 = plt.figure(figsize=(10,10))
hist15 = sns.histplot(
    data = df_final,
    x = 'Confidence level (range)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist15.set_ylabel('Proportion of clients', fontsize = 30)
hist15.set_xlabel('Confidence level', fontsize = 30)
hist15.set_title('Objective variable depending on the Confidence level', fontsize = 35)
for container in hist15.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist15.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Employment variation (range): Estudiamos la distribución de Yes y No en función de la tasa de variación del empleo
fig16 = plt.figure(figsize=(10,10))
hist16 = sns.histplot(
    data = df_final,
    x = 'Employment variation (range)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist16.set_ylabel('Proportion of clients', fontsize = 30)
hist16.set_xlabel('Employment variation', fontsize = 30)
hist16.set_title('Objective variable depending on the employment variation rate', fontsize = 35)
for container in hist16.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist16.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Annual income (range): Estudiamos la distribución de Yes y No en función del salario anual de los clientes
fig17 = plt.figure(figsize=(10,10))
hist17 = sns.histplot(
    data = df_final,
    x = 'Annual income (range)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist17.set_ylabel('Proportion of clients', fontsize = 30)
hist17.set_xlabel('Annual income', fontsize = 30)
hist17.set_title('Objective variable depending on the annual income', fontsize = 35)
for container in hist17.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist17.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE # Kids at home: Estudiamos la distribución de Yes y No en función del número de niños en casa del cliente
fig18 = plt.figure(figsize=(10,10))
hist18 = sns.histplot(
    data = df_final,
    x = '# Kids at home',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist18.set_ylabel('Proportion of clients', fontsize = 30)
hist18.set_xlabel('# Kids at home', fontsize = 30)
hist18.set_title('Objective variable depending on the number of kids at home', fontsize = 35)
for container in hist18.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist18.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
#Incluimos 3 líneas nuevas para modificar los ticks del eje X. Hacemos que sean números enteros, y que vayan de 1 en 1, en vez 0.5 en 0.5
ticks = range(0, 2 + 1)
hist18.set_xticks(ticks)
hist18.set_xticklabels(ticks, fontsize=20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE # Teens at home: Estudiamos la distribución de Yes y No en función del salario anual de los clientes
fig19 = plt.figure(figsize=(10,10))
hist19 = sns.histplot(
    data = df_final,
    x = '# Teens at home',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist19.set_ylabel('Proportion of clients', fontsize = 30)
hist19.set_xlabel('# Teens at home', fontsize = 30)
hist19.set_title('Objective variable depending on the number of teens at home', fontsize = 35)
for container in hist19.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist19.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
#Incluimos 3 líneas nuevas para modificar los ticks del eje X. Hacemos que sean números enteros, y que vayan de 1 en 1, en vez 0.5 en 0.5
ticks = range(0, 2 + 1)
hist19.set_xticks(ticks)
hist19.set_xticklabels(ticks, fontsize=20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

# VARIABLE Web visit freq. (per month): Estudiamos la distribución de Yes y No en función de la frecuencia con la que visitan
#los clientes nuestra web
fig20 = plt.figure(figsize=(10,10))
hist20 = sns.histplot(
    data = df_final,
    x = 'Web visit freq. (per month)',
    hue = 'Objective variable',
    palette = 'pastel',
    multiple = 'fill',
    stat = 'proportion',
    discrete = True,
    shrink = .7
)
hist20.set_ylabel('Proportion of clients', fontsize = 30)
hist20.set_xlabel('Frequency of website visit', fontsize = 30)
hist20.set_title('Objective variable depending on the website visit frequency', fontsize = 35)
for container in hist20.containers:
    labels_list = []
    for bar in container:
        label = f'{np.round(bar.get_height() * 100,2)}%'
        labels_list.append(label)
    hist20.bar_label(container, labels = labels_list, label_type = 'center', fontsize = 30)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.show()

#3. Evolución del porcentaje de éxito en función de la fecha de contacto: Como hemos visto en nuestra tabla principal, tenemos una columna
#que nos indica la fecha en la que el cliente fue contactado, la cual, durante el EDA, he dividido en mes año. Podemos aprovecharnos de esos
#datos para observar, en un gráfico de líneas, cómo evoluciona el porcentaje de éxito de nuestra variable objetivo con el tiempo, en función
#del año y mes en el que fueron contactados los clientes:
df_final['Contact date (year)'] = df_final['Contact date (year)'].astype("string") #Para esta representación, en primer lugar convertimos la
#la columna 'Contact date (year)' en string, ya que más tarde la vamos a unir a otra columna
def transformar_meses(mes): #Creamos una función que nos permita transformar el nombre de los meses en su correspondiente número
    if mes == 'January':
        return '01'
    if mes == 'February':
        return '02'
    if mes == 'March':
        return '03'
    if mes == 'April':
        return '04'
    if mes == 'May':
        return '05'
    if mes == 'June':
        return '06'
    if mes == 'July':
        return '07'
    if mes == 'August':
        return '08'
    if mes == 'September':
        return '09'
    if mes == 'October':
        return '10'
    if mes == 'November':
        return '11'
    if mes == 'December':
        return '12'
    else:
        return 'No informado'
df_final['Contact date (month)'] = df_final['Contact date (month)'].apply(transformar_meses) #Aplicamos dicha función a nuestra columna
suma_fechas = df_final['Contact date (year)'] + '-' + df_final['Contact date (month)'] #Creamos una nueva variable, en la que juntaremos el
#el año de contacto con el mes de contacto
df_final = df_final.assign(complete_date = suma_fechas) #Crearemos una nueva columna, cuyo contenido será dicha variable, de manera que
#obtenemos una fecha con el formato 'yyyy-mm'
#Ahora, creamos dos dataframes, filtrados en función del valor de nuestra variable objetivo (Yes o No), y agruparemos cada uno en función de
#la columna 'complete date'; además, contaremos los valores obtenidos para cada grupo creado, y resetearemos el índice para evitar futuros errores
df_final0 = df_final[df_final['Objective variable'] == 'No'].groupby('complete_date')['Objective variable'].count().reset_index()
df_final1 = df_final[df_final['Objective variable'] == 'Yes'].groupby('complete_date')['Objective variable'].count().reset_index()
df_linechart = df_final0.merge(df_final1, how = 'inner', on = 'complete_date') #Una vez creados, haremos merge entre los dos dataframes por la
#columna complete_date, de manera que queden unidos por dicha columna
#Tras esto, crearemos dos columnas en las que, para cada grupo, sacaremos el porcentaje de Yes y el de No en función a la cantidad de datos totales
#para dicho grupo. Tras ello, asignaremos dichas columnas al último dataframe que habíamos creado
nueva_columna1 = (df_linechart['Objective variable_x']/(df_linechart['Objective variable_x'] + df_linechart['Objective variable_y'])) * 100
nueva_columna2 = (df_linechart['Objective variable_y']/(df_linechart['Objective variable_x'] + df_linechart['Objective variable_y'])) * 100
df_linechart = df_linechart.assign(porcentaje_no = nueva_columna1, porcentaje_si = nueva_columna2)
#Una vez completado el dataframe, haremos un cambio de nombre en las columnas para que los títulos sean más intuitivos y cortos
df_linechart.rename(columns = {'complete_date': 'Complete date',
                               'Objective variable_x': 'No',
                               'Objective variable_y': 'Yes',
                               'porcentaje_no': '% No',
                               'porcentaje_si': '% Yes'
                               }, inplace = True)
#Tras ello, convertiremos el formato de nuestra columna 'Complete date' a fecha, con el método pd.to_datetime()
df_linechart['Complete date'] = pd.to_datetime(df_linechart['Complete date'])
#Por último, usaremos la función pd.melt(), aprendida en este curso, para 'fusionar' las columnas '% No' y '% Yes', de manera que la representación
#con seaborn sea más sencilla
df_linechart = pd.melt(df_linechart, id_vars = 'Complete date', value_vars = ['% No', '% Yes'], var_name = 'Response', value_name = 'Percentage')
print(df_linechart.head(10)) #Comprobación del resultado final de nuestro dataframe

fig1 = plt.figure(figsize=(10,10)) #Creación del objeto figura
line1 = sns.lineplot( #Diseñamos una gráfica de líneas con seaborn. Pasamos el dataframe, las columnas para los ejes X y Y, y el 'hue', que nos
    #permitirá diferenciar dos objetos diferentes en la misma gráfica, los cuales vendrán determinados por el parámetro 'Response'. Esta es la
    #razón por la que aplicamos el método melt() previamente. Ajustamos el formato con palette, marker y markersize
    data = df_linechart,
    x = 'Complete date',
    y = 'Percentage',
    hue = 'Response',
    palette = 'Set2',
    marker = 'o',
    markersize = 5
)
#Títulos y formato de los ejes y del gráfico
line1.set_ylabel('Percentage of the value', fontsize = 30)
line1.set_xlabel('Contact date', fontsize = 30)
line1.set_title('Evolution of subscription to product/services through the years', fontsize = 35)
#Distribución y formato de los ticks de los ejes
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(np.arange(0,110,step = 10), fontsize = 20)
#Ajustamos el tamaño y mostramos la gráfica
plt.tight_layout()
plt.show()

#Esta última representación resulta muy interesante, ya que podemos observar la evolución de la contratación de los productos/servicios a lo largo
#de los años para muchos de los subgrupos que hemos estudiado previamente. Voy a realizar únicamente un ejemplo para no saturar más el proyecto con
#visualizaciones, pero será un ejemplo muy ilustrativo. De entre todas las variables estudiadas, hemos visto que la duración de la última llamada
#con el cliente fue una variable que influía fuertemente en su decisión con respecto a suscribirse a un producto/servicio. Por tanto, en función del
#número de llamadas que recibió el cliente, quizás podemos observar un comportamiento interesante de las suscripciones a lo largo de los años.
df_final['Contact date (year)'] = df_final['Contact date (year)'].astype("string") #Para esta representación, en primer lugar convertimos la
#la columna 'Contact date (year)' en string, ya que más tarde la vamos a unir a otra columna
def transformar_meses(mes): #Creamos una función que nos permita transformar el nombre de los meses en su correspondiente número
    if mes == 'January':
        return '01'
    if mes == 'February':
        return '02'
    if mes == 'March':
        return '03'
    if mes == 'April':
        return '04'
    if mes == 'May':
        return '05'
    if mes == 'June':
        return '06'
    if mes == 'July':
        return '07'
    if mes == 'August':
        return '08'
    if mes == 'September':
        return '09'
    if mes == 'October':
        return '10'
    if mes == 'November':
        return '11'
    if mes == 'December':
        return '12'
    else:
        return 'No informado'
df_final['Contact date (month)'] = df_final['Contact date (month)'].apply(transformar_meses)
suma_fechas = df_final['Contact date (year)'] + '-' + df_final['Contact date (month)']
df_final = df_final.assign(complete_date = suma_fechas)
df_final1 = df_final[df_final['Objective variable'] == 'Yes']
df_final0 = df_final[df_final['Objective variable'] == 'No']
df_llamada_corta1 = df_final1[df_final1['Last call (range)'] == '0-5 minutes'].groupby('complete_date')['Objective variable'].count().reset_index()
df_llamada_larga1 = df_final1[df_final1['Last call (range)'] == '15-30 minutes'].groupby('complete_date')['Objective variable'].count().reset_index()
df_llamada_corta0 = df_final0[df_final0['Last call (range)'] == '0-5 minutes'].groupby('complete_date')['Objective variable'].count().reset_index()
df_llamada_larga0 = df_final0[df_final0['Last call (range)'] == '15-30 minutes'].groupby('complete_date')['Objective variable'].count().reset_index()

print(df_llamada_larga1, df_llamada_corta1, df_llamada_corta0, df_llamada_larga0)
df_corta = df_llamada_corta1.merge(df_llamada_corta0, how = 'inner', on = 'complete_date')
df_corta.rename(columns = {'complete_date': 'Complete date',
                               'Objective variable_x': 'Yes_corta',
                               'Objective variable_y': 'No_corta'
                               }, inplace = True)
df_larga = df_llamada_larga1.merge(df_llamada_larga0, how = 'inner', on = 'complete_date')
df_larga.rename(columns = {'complete_date': 'Complete date',
                               'Objective variable_x': 'Yes_larga',
                               'Objective variable_y': 'No_larga'
                               }, inplace = True)
df_def = df_corta.merge(df_larga, how = 'inner', on = 'Complete date')
print(df_corta.head())
print(df_larga.head())
nueva_columna1 = (df_def['No_corta']/(df_def['No_corta'] + df_def['Yes_corta'])) * 100
nueva_columna2 = (df_def['Yes_corta']/(df_def['No_corta'] + df_def['Yes_corta'])) * 100
nueva_columna3 = (df_def['No_larga']/(df_def['No_larga'] + df_def['Yes_larga'])) * 100
nueva_columna4 = (df_def['Yes_larga']/(df_def['No_larga'] + df_def['Yes_larga'])) * 100
df_def = df_def.assign(porcentaje_no_corta = nueva_columna1,
                                   porcentaje_si_corta = nueva_columna2,
                                   porcentaje_no_larga = nueva_columna3,
                                   porcentaje_si_larga = nueva_columna4)
df_def.rename(columns = {'porcentaje_no_corta': '% No_corta',
                               'porcentaje_si_corta': '% Yes_corta',
                               'porcentaje_no_larga': '% No_larga',
                               'porcentaje_si_larga': '% Yes_larga'
                               }, inplace = True)
df_def['Complete date'] = pd.to_datetime(df_def['Complete date'])
df_def = pd.melt(df_def, id_vars = 'Complete date', value_vars = ['% Yes_corta', '% Yes_larga'], var_name = 'Response', value_name = 'Percentage')
print(df_def.head(10))
fig2 = plt.figure(figsize=(10,10))
line2 = sns.lineplot(data = df_def,
    x = 'Complete date',
    y = 'Percentage',
    hue = 'Response',
    palette = 'Set2',
    marker = 'o',
    markersize = 5
)
line2.set_ylabel('Percentage of the value', fontsize = 30)
line2.set_xlabel('Contact date', fontsize = 30)
line2.set_title('Evolution of subscription to product/services through the years', fontsize = 35)
plt.xticks(rotation = 0, fontsize = 20)
plt.yticks(np.arange(0,110,step = 10), fontsize = 20)
plt.tight_layout()
plt.show()

#El código es un poco más laborioso, pero sigue la misma estructura, que se puede complicar más en función de las variables que se incluyan. Aquí podemos comprobar,
#por ejemplo, que el éxito en la contratación de servicios o productos es bastante bajo y estable cuando la última llamada con el cliente dura de 0 a 5 minutos.
#Sin embargo, cuando la llamada del cliente dura 15-30 minutos, podemos observar, no solamente que la proporción de éxito en la contratación es mucho más alta, sino
# que también fluctúa más a lo largo del tiempo, con picos más pronunciados a lo largo de los años.
#El código es un poco más laborioso, pero sigue la misma estructura, que se puede complicar más en función de las variables que se incluyan. Aquí podemos comprobar,
#por ejemplo, que el éxito en la contratación de servicios o productos es bastante bajo y estable cuando la última llamada con el cliente dura de 0 a 5 minutos.
#Sin embargo, cuando la llamada del cliente dura 15-30 minutos, podemos observar, no solamente que la proporción de éxito en la contratación es mucho más alta, sino
# que también fluctúa más a lo largo del tiempo, con picos más pronunciados a lo largo de los años.