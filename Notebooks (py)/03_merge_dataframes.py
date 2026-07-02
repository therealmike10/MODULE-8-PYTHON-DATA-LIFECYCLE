import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl
import os

#MERGE DE TABLAS PRINCIPAL Y AUXILIAR
pd.set_option('display.max_columns', None)
tabla_principal = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/01_EDA_bank_additional.csv"
tabla_auxiliar = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/02_EDA_customer_details.csv"
df_principal = pd.read_csv(tabla_principal, index_col = 0)
df_auxiliar = pd.read_csv(tabla_auxiliar, index_col = 0)
#Una vez cargadas correctamente, usamos el método merge para unirlas por la única columna en la que pueden coincidir ambas tablas: Client ID
df_final = df_principal.merge(df_auxiliar, how = 'inner', on = 'Client ID')
print(df_final.head(10))
print(df_final.shape)
print(df_final.info())
print(df_final.isnull().sum())
print(df_final.isna().sum())
#Como podemos comprobar, nuestro merge se ha ejecutado correctamente, a juzgar por las 10 primeras filas de la tabla. Tenemos, además, un total de 42752 filas
#y 33 columnas; el número de filas coincide con el número de las filas de la tabla principal, al haberla establecido como la tabla izquierda y haber hecho un
#'inner merge'. La tabla auxiliar tenía un total de 43171 filas, por lo que en el merge() hemos perdido alguna fila; esto es normal, ya que la tabla principal
#se ha sometido a una limpieza más exhaustiva, y debido a ello algunas filas tuvieron que ser eliminadas. El número de filas obtenidas tras el merge, por tanto,
#está dentro de lo esperado. Además, también podemos comprobar que no hay varios null en todo nuestro dataframe, gracias a los EDA previamente realizados


#GUARDADO DE LA TABLA LIMPIA EN .CSV
#Una vez hemos realizado el merge, guardamos nuestro dataframe definitivo en formato .csv. Esto nos permitirá importar este .csv de nuevo como un dataframe
#en un último archivo .py, que estará destinado a llevar a cabo las diferentes visualizaciones de los datos.
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL', exist_ok = True)
df_final.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/03_merge_dataframes.csv')

