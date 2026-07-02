import pandas as pd
import numpy as np
import os
import openpyxl

#LIMPIEZA DE DATOS 'customer-details'
#Una vez realizado el EDA en nuestra tabla principal, procedemos a unirla con las diferentes hojas del archivo 'customer_details.xlsx'. En primer lugar,
#importamos los datos de nuestro archivo xlsx, para poder tener en forma de dataframe. Lo hacemos para las 3 hojas existentes:
#NOTA: Para leer archivos .xlsx, he tenido que instalar el módulo 'openpyxl', ya que de otra manera, obtenía un error.
pd.set_option('display.max_columns', None)
file1 = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/DatosProyecto/customer-details.xlsx"
df_details1 = pd.read_excel(file1, sheet_name = '2012', index_col = 0)
df_details2 = pd.read_excel(file1, sheet_name = '2013', index_col = 0)
df_details3 = pd.read_excel(file1, sheet_name = '2014', index_col = 0)
#Imprimimos los nombres de las columnas antes de concatenar los dataframes, para asegurarnos que tienen el mismo nombre, y por tanto se unen correctamente
print(df_details1.columns)
print(df_details2.columns)
print(df_details3.columns)
details_concat = pd.concat([df_details1, df_details2, df_details3], ignore_index = True) #Con ignore_index, ignoramos los índices anteriores y lo reseteamos
#Comprobamos las 10 últimas filas, para asegurar que se han unido correctamente, y pedimos a pandas que nos devuelva los detalles del tamaño del dataframe
print(details_concat.tail(10))
print(details_concat.shape)
#Una vez hemos cargado nuestros dataframes, realizamos un ajuste de las columnas y sus datos, como hemos hecho previamente en nuesrto dataframe principal, antes de
#unir ambos.
print(details_concat.info())
#Vemos, gracias al método info(), que no tenemos nigún valor null para ninguna de las columnas de nuestro dataframe auxiliar. Ahora, en primer lugar, vamos a guardar
# las estadísticas descriptivas de las columnas con variables numéricas, ya que, al igual que en la tabla principal, transformaremos varias en variables categóricas:
#GUARDADO DE ESTADÍSTICAS DESCRIPTIVAS EN ARCHIVO .CSV
descripcion_auxiliar = details_concat[['Income', 'Kidhome', 'Teenhome', 'NumWebVisitsMonth']].describe()
print(descripcion_auxiliar)
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL', exist_ok = True)
descripcion_auxiliar.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/descriptive_statistics_details.csv')
#Tras esto, vamos a realizar las modificaciones pertinentes en el resto de columnas, para transformar datos y homogeneizar formatos
    #- COLUMNA 'Income'
details_concat['Income'] = details_concat['Income'].astype(dtype = 'float64')
print(details_concat['Income'].describe())
income_min = details_concat['Income'].min()
income_q1 = details_concat['Income'].quantile(0.25)
income_q3 = details_concat['Income'].quantile(0.75)
print(income_min)
print(income_q1)
print(income_q3)
def income_range(salary):
    if income_min <= salary <= income_q1:
        return 'Low salary [< 49,608.00]'
    elif income_q1 < salary <= income_q3:
        return 'Medium salary [49,608.00 - 136,740.00]'
    else:
        return 'High salary [> 136,740.00]'
details_concat['Annual income (range)'] = details_concat['Income'].apply(income_range)
    #- COLUMNA 'Kidhome'
print(details_concat['Kidhome'].describe())
#Vemos que el mínimo es 0 y el máximo es 2, así que no merece la pena crear una columna con variables categóricas. Dejamos esta columna como está.
    #- COLUMNA 'Teenhome'
print(details_concat['Teenhome'].describe())
#De manera similar al anterior, el mínimo es 0 y el máximo es 2, así que no merece la pena crear una columna con variables categóricas.
    #- COLUMNA 'NumWebVisitsMonth'
print(details_concat['NumWebVisitsMonth'].describe())
visits_minimo = details_concat['NumWebVisitsMonth'].min()
print(visits_minimo)
def visit_frequence(visit):
    if visits_minimo <= visit <= 10:
        return 'Occasional (1 - 10)'
    elif 10 < visit <= 20:
        return 'Frequent (10 - 20)'
    else:
        return 'Highly frequent (> 20)'
details_concat['Web visit freq. (per month)'] = details_concat['NumWebVisitsMonth'].apply(visit_frequence)

    #- COLUMNA Dt_Customer
#Para esta columna, al estar en formato datetime64[ns], podemos usar el método .dt para extraer el mes y el año en el que el cliente se dio de alta.
details_concat = details_concat.assign(register_month = details_concat['Dt_Customer'].dt.strftime("%B"), register_year = details_concat['Dt_Customer'].dt.year)
#Indagando un poco en internet sobre el método .dt, encontré que, cuando se combina con strftime, puedes elegir que parte del 'datetime' quieres que te devuelva
#en diferentes formatos. Usando strftime("%B"), puedo obtener los meses en formato .title(), con el nombre completo y en inglés sin necesidad de aplicar una
#fórmula larga como hice en la tabla principal.
details_concat.drop(columns=['Dt_Customer'], inplace=True)
#El resto de los valores no aportan mucha información, ya que el día no aporta mucha información a nivel categórico, y la hora es 00:00:00 para todos los datos
#(aunque no fuera así, tampoco aporta mucha más información). Por tanto, decidimos borrar la columna.
#Finalmente, al igual que en la tabla principal, realizamos los cambios finales de nombre de las columnas y su orden, último paso previo antes de unirlas
details_concat.rename(columns = {'Income': 'Annual income (EUR)',
                                 'Kidhome': '# Kids at home',
                                 'Teenhome': '# Teens at home',
                                 'ID': 'Client ID', #MUY IMPORTANTE: Este nombre tiene que coincidir con el de la tabla principal, ya que será la columna por la que se unan
                                 'register_month': 'Register date (month)',
                                 'register_year': 'Register date (year)',
                                 'NumWebVisitsMonth': 'Web visit freq.'
                                 }, inplace = True)
details_concat = details_concat[['Client ID', 'Annual income (EUR)', 'Annual income (range)', '# Kids at home', '# Teens at home', 'Web visit freq.',
                                 'Web visit freq. (per month)', 'Register date (month)', 'Register date (year)']]
print(details_concat.head(10))
print(details_concat.info())

#Por último, y como medida cautelar final, realizamos una breve prueba para comprobar si, después de todos los pasos de limpieza y exploración realizados,
#hubies algún dato duplicado en nuestro dataframe
duplicates = details_concat[details_concat.duplicated()]
print(duplicates)
#El print nos devuelve 'Empty DataFrame', con lo que nos aseguramos de que no hay datos duplicados

#GUARDADO DE LA TABLA LIMPIA EN .CSV
#Una vez hemos terminado el EDA de nuestra tabla auxiliar, guardamos los datos en formato .csv. Esto nos permitirá importar este .csv de nuevo como un dataframe
#en un nuevo archivo .py, que estará destinado a realizar el merge con la tabla principal y, en otro destinado a llevar a cabo las diferentes visualizaciones de los datos.
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL', exist_ok = True)
details_concat.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/02_EDA_customer_details.csv')