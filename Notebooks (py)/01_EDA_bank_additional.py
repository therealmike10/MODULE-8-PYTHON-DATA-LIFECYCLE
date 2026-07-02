#PROYECTO LÓGICA: PROYECTO EDA CON PYTHON
#Autor: Miguel Encinas Gimenez

#IMPORTANTE: Debido a haber realizado el curso de 'IBM Tools for Data Science' con anterioridad, he podido aplicar algunos razonamientos y métodos puntuales que,
#a pesar de no haber sido vistos en estes cursos, he considerado útiles a la hora de aplicarlos en este proyecto, sobre todo aquellos que tienen que ver con pandas.
#No son métodos o razonamientos mucho más complejos que los aquí enseñados, y están debidamente explicados con comentarios. Por otro lado, el código estará dividido
#en bloques, en función de las tareas que se realicen en dicho bloque (eliminación de nulls, creación de columnas, manipulación de datos, etc.).

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl
import os

#BLOQUE DE CARGA DE NUESTROS DATOS E INFORMACIÓN BÁSICA
#En primer lugar, cargamos nuestro archivo csv en un dataframe de pandas. Le indicamos que la primera columna va a ser nuestra columna de indexación,
#ya que es la columna con el número de la entrada de los datos.
file = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/DatosProyecto/bank-additional.csv"
df_clientes = pd.read_csv(file, index_col= 0)

#Tras esto, imprimimos las 10 primeras filas de nuestro dataframe para estudiar los datos. Como tenemos muchas columnas, le pedimos
#que nos las muestre tdoas con set_option.
pd.set_option('display.max_columns', None)
print(df_clientes.head(10))

#También solicitamos a pandas la información principal de nuestro archivo, así como el número de datos faltantes.
print(df_clientes.info())
print(df_clientes.isnull().sum())
print(df_clientes.isna().sum())

#Tareas a realizar:
'''
ESQUEMA DE TRABAJO
1. Eliminar los NaN o los null, y decidir qué hacer con las filas correspondientes:
    - age: Como agruparé en un futuro, crear una categoría de 'no informado' --Hecho
    - job: son pocos y agruparé. Crear categoría de 'no informado' --Hecho
    - marital: son muy pocos. Crear categoría de no informado o sustituir por más común --Hecho
    - education: Seguramente crear una categoría de no informado, ya que agruparé por categorías para el estudio de los datos --Hecho
    - default: informa si tiene deudas. 34k son 'No' vs 3 'Sí', y faltan 8k datos. Dropeo columna porque no es útil --Hecho
    - housing: Bastante igualado el sí y no, quizás sustituyo por 'no informado'. No veo claro sustituir por más común --Hecho
    - loan: 35k vs 6k. Sustituyo por más común, dropeo columna o 'no informado'.Cualquiera me parece bien -- Hecho
    - cons.price.idx: Muy pocos null, sustituiré por la media por la media --Hecho
    - euribor3m. 1/5 parte null, o sustituyo por la media o dropeo ya que son muchos null --Hecho
    - date: pocos NaN, creo que puedo dropear ya que me interesa saber el mes y el año a priori --Hecho
2. Eliminar columna longitude, latitude y nr.employed, ya que no la vamos a necesitar o no parecen útiles--Hecho
3. Añadir las columnas de contact_month y contact_year, ya que están en el informe pero no en los datos. Cambiar a int la columna de los años --Hecho
    3.1. Eliminar la columna date y quedarme solo con las de mes y año --Hecho
4. Guardar el .describe() de las columnas de variables numéricas antes de realizar la agrupación en variables categóricas --Hecho
5. Realizar agrupaciones en función de los datos --Hecho
    - Nivel de estudios --Hecho
    - Trabajo --Hecho
    - Rango de ingresos anuales --Hecho
    - Edad --Hecho
    - Duración llamada --Hecho
    - IPC --Hecho
    - Confianza del consumidor --Hecho
    - Ratio de variabilidadd de empleo --Hecho
6. Unir la tabla principal con la tabla de customer_details
7. Mirar cómo afectan diferentes condiciones a decir si un cliente se ha suscrito o no a un servicio
    - Método de contacto
    - Estudios
    - Estado marital
    - Trabajo
    - Número de contactos realizados durante la campaña.
    - Número de veces contactados antes de la campaña.

'''
# BLOQUE MODIFICACIÓN COLUMNAS + ELIMINACIÓN/SUSTITUCIÓN DE NaN, null
#Vamos a ir tratando, una por una, todas las columnas que poseen algún elemento NaN, según hemos visto con los métodos .isnull() e .isna()
#COLUMNA 'age' - Para esta coluimna, tenemos un valor null para algo más de un 10% de las filas en nuestro conjunto de datos. Como es probable
#que para el estudio de esta variable agrupemos por rango de edad, vamos a sustituir esos null por el valor 'No informado', para no perder esos datos
print(df_clientes['age'].isnull().sum())
df_clientes.fillna(
    {'age': 0},
     inplace = True)
#Como no va a haber ningún cliente de '0' años, hemos sustituidos las columnas null por 0, para poder convertir así la columna a int, lo cual nos facilitará
#posteriormente su clasificación en grupos categóricos.
df_clientes['age'] = df_clientes['age'].astype("int64")


#COlUMNA 'job' - Mismo razonamiento, en este caso el número de valores null es muy bajo (345), y los valores están muy repartidos así que crearé una
#categoría de 'No informado' nuevamente.
distrib_trabajo = df_clientes['job'].value_counts()
print(df_clientes['job'].isnull().sum())
print(distrib_trabajo)
df_clientes.fillna(
    {'job': 'Not informed'},
    inplace = True)
#Aplicamos el método .title() para que las palabras empiecen por mayúscula, simplemente por igualar formatos entre columnas.
df_clientes['job'] = df_clientes['job'].str.title()

#COLUMNA 'marital' - En este caso, tenemos 85 valores null para 43,000 datos totales. Considerando que el estado 'MARRIED' es predominante con respecto
#a los otros dos, en vez de crear una categoría única de 'no informado' solo para 85 valores, vamos a sustituir los null por la categoría más comúnmente
#repetida, que es 'MARRIED'
distrib_marital = df_clientes['marital'].value_counts()
print(distrib_marital)
print(df_clientes['marital'].isnull().sum())
df_clientes.fillna(
    {'marital': 'MARRIED'},
    inplace = True)
#Aplicamos el método .title() para que las palabras empiecen por mayúscula y sigan en minúsucla, simplemente por igualar formatos entre columnas.
df_clientes['marital'] = df_clientes['marital'].str.title()

#COLUMNA 'education' - Tanto la categoría 'university.degree' como la categoría 'high.school' poseen un número similar de datos, en comparación con el resto
#de categorías. Por tanto, la adición de los 1807 valores null a cualquiera de las dos categorías podrías alterar el estudio de los datos. Debido a ello, creo
#que lo mejor sería crear una nueva categoría llamada 'No informado', como en otras columnas
distrib_educacion = df_clientes['education'].value_counts()
print(distrib_educacion)
print(df_clientes['education'].isnull().sum())
df_clientes.fillna(
    {'education': 'Not informed'},
    inplace = True)

#Columna 'default' - Con esta columna pasa algo diferente que con las anteriores. De las 43,000 filas totales que disponemos, tenemos ~34,000 con el valor 0 (No),
#y solo 3 columnas con el valor 1 (Sí). Por un lado, la presencia de 8,981 valores null es bastante elevada, así que la primera opción sería crear una categoría de
#'No informado'. Sin embargo, teniendo en cuenta que prácticamente todos los datos de esa columna son 0 (No), considero que ese dato no aporta información útil en
#este caso. Por lo tanto, creo que lo mejor es eliminar la columna mediante el uso del método .drop(), ya que la amplia mayoría de clientes no presenta incumplimiento de pagos
distrib_impagos = df_clientes['default'].value_counts()
print(distrib_impagos)
print(df_clientes['default'].isnull().sum())
df_clientes.drop(columns = ['default'], inplace = True)

#COLUMNA 'housing' - Esta columna indica si el cliente tiene un préstamo hipotecario. Los valores de 0 (No) y 1 (Sí) están bastante igualados, así que, teniendo en cuenta
#que tenemos ~1,000 valores null, creo que la opción de sustituir por el más común no es la más correcto. Por tanto, crearé nuevamente la categoría de 'No informado'
distrib_hipoteca = df_clientes['housing'].value_counts()
print(distrib_hipoteca)
print(df_clientes['housing'].isnull().sum())
df_clientes.fillna(
    {'housing': 'Not informed'},
    inplace = True)
#Además, vamos a reemplazar los códigos numéricos 0 y 1 por 'No' y 'Yes', para facilitar así el entendimiento de los datos
df_clientes['housing'] = df_clientes['housing'].replace(0, 'No').replace(1, 'Yes')

#COLUMNA 'loan' - Esta columna indica si el cliente tiene algún otro tipo de préstamo. En este caso, tenemos unos 35,000 datos 0 (No), y unos 6,000 datos 1 (Sí). Considerando
#que hay unos nuevamente unos 1,000 datos null, y la diferencia entre respuestas es tan grande, creo que lo más conveniente es sustituir los valores null por el más común (0)
distrib_loan = df_clientes['loan'].value_counts()
print(distrib_loan)
print(df_clientes['loan'].isnull().sum())
df_clientes.fillna(
    {'loan': 0},
    inplace = True)
#Además, vamos a reemplazar los códigos numéricos 0 y 1 por 'No' y 'Yes', para facilitar así el entendimiento de los datos
df_clientes['loan'] = df_clientes['loan'].replace(0, 'No').replace(1, 'Yes')

#COLUMNA 'duration' - Esta columna indica cuánto tiempo duró la última llamada que se realizó al cliente. Por tanto, será mucho más intuitivo
#si esa llamada está en minutos en vez de ne segundos, a pesar de tener decimales en el resultado
df_clientes['duration'] = np.round(df_clientes['duration']/60, 1)

#COLUMNA 'cons.price.idx' - Esta columna nos indica los índices de precios al consumidor. En este caso es un valor numérico, para el que hay menos de 500 valores null.
#Estudiando los datos, a pesar de que podría parecer que es una variable continua, el recuento de valores parece devolver únicamente 26 valores discretos, lo cual es
#un número relativamente bajo para una columna de integers en una tabla de 43,000 filas. Por tanto, se podría valorar la opción de sustituir los null por el valor más
#frecuente (93,994), pero en este caso voy a optar por sustituir por el valor de la media de los datos de dicha columna, ya que tampoco aparecen valores outliers.
print(df_clientes['cons.price.idx'].isnull().sum())
ipc_valores = df_clientes['cons.price.idx'].value_counts()
print(ipc_valores)
#Reemplazamos, celda por celda, los elementos dentro de la celda que indicamos en replace(), por eso usamos .str.
df_clientes['cons.price.idx'] = df_clientes['cons.price.idx'].str.replace(',','.').str.replace('"','')
#Transformamos los valores a número para poder operar con ellos
df_clientes['cons.price.idx'] = pd.to_numeric(df_clientes['cons.price.idx'])
#Calculamos la media de toda la columna y la redondeamos a 3 decimales
ipc_media = np.round(df_clientes.loc[:, 'cons.price.idx'].mean(), decimals = 3)
#Sustituimos los null por el valor de la media
df_clientes['cons.price.idx'] = df_clientes['cons.price.idx'].fillna(ipc_media)
#Aprovechamos para cambiar el tipo de datos en la columna a float64
df_clientes['cons.price.idx'] = df_clientes['cons.price.idx'].astype("float64")

#COLUMNA 'euribor3m' - Valore del euribor a 3 meses. Cabe destacar que faltan bastantes datos, y he querido estudiarlo con detenimiento:
#En primer lugar, confirmamos que faltan más de 9,000 datos para esta columna
print(df_clientes['euribor3m'].isnull().sum())
#Tras esto, calculamos ahora la media y la desviación estándar de la columna, transformando previamente la columna a numérico:
df_clientes['euribor3m'] = df_clientes['euribor3m'].str.replace(',','.').str.replace('"','')
df_clientes['euribor3m'] = pd.to_numeric(df_clientes['euribor3m'])
euribor_media = np.round(df_clientes.loc[:, 'euribor3m'].mean(), decimals = 3)
euribor_std = np.round(df_clientes.loc[:, 'euribor3m'].std(), decimals = 3)
print([euribor_std, euribor_media])
#Podemos observar que obtenemos una media de 3.617, pero también una desviación estándar 1.737. Esto quiere decir que, para nuestro conjunto de datos
#el valor de la media puede variar casi un 50% (en ambas direcciones) con respecto al valor de la media. Esto, junto con el hecho de que faltan más de
#1/5 parte de los datos de la columna 'euribor3m', y que no lo considero un dato especialmente relevante para nuestro conjunto, me lleva a la conclusión
#de que la opción óptima es eliminar dicha columna
df_clientes.drop(columns = ['euribor3m'], inplace = True)

#COLUMNA 'date' - En esta columna tenemos un número muy bajo de datos null (248); además, considero relevante saber la fecha en la que se realizó la interacción
#con cada cliente. Por tanto, sustituiremos los datos null por 'No informado'. Para esto, empezaremos generando las columans 'contact_month' y 'contact_year',
# refiriéndose al mes y el año en el que ser realizó la interacción con el cliente durante la campaña de marketing. Estas columnas están en el informe proporcionado,
# pero no está en el documento .csv de los datos; por tanto, las podemos crear a partir de la columna 'date', extrayendo el mes y el año. Para ello, vamos a aplicar
# métodos vectorizados con .str, es decir. El uso de #este método se puede combinar con muchos de los métodos que hemos visto en la lección de Python para usar en strings.
df_clientes['date(list)'] = df_clientes['date'].str.split('-') #Creamos una columna con las entradas de las fechas, en formato lista separada por '-'.
#Tras esto, creamos nuestras dos nuevas columnas: contact_month, tomando el mes de la columna 'date(list)' (elemento 1) y poniéndolo en mayúsculas;
#y la columna 'contact_year', tomando el año de la misma columna (elemento 2).
df_clientes2 = df_clientes.assign(contact_month = df_clientes['date(list)'].str[1].str.title(), contact_year = df_clientes['date(list)'].str[2])
#En este caso, nos interesa saber los años y meses en los que se produjo cada interacción con el cliente. Disponemos solamnete de 248 valores null, así que he considerado
#que lo más apropiado en este caso sería eliminar esas 248 entradas para las que no tenemos fecha, ya que no tiene sentido desconocer la fecha de interacción con el cliente.
filas_a_eliminar = df_clientes2[df_clientes2['contact_year'].isnull()].index
df_clientes2.drop(filas_a_eliminar, axis = 0, inplace = True)
#Una vez hemos eliminado los null, convertimos la columna 'contact_year' al tipo 'int64'.
df_clientes2['contact_year'] = df_clientes2['contact_year'].astype("int64")

#Siguiendo con el tratamiento de columnas, hay varias columnas que me interesa eliminar a pesar de que no tengan valores null, ya que considero que no son de utilidad:
    # -'longitude' y 'latitude': Estas columnas no figuran en el informe proporcionado, por lo tanto, aunque podemos suponer que hacen referencia a la geolocalización
    # de cada cliente, no podemos saberlo con certeza. Debido a esto, lo más prudente es no contar con ellas para este análisis
    # -'nr.employed': En el informe proporcionado, se refiere al 'número de empleados'. Sin embargo, con una rápida búsqueda en el archivo csv proporcionado, podemos comprobar
    # que es una variable discreta con pocos valores, pero la mayoría de ellos son decimales. Esto no tiene mucho sentido si la columna se refiere a número de empleados. Cabe
    # la posibilidad de que sea una errata y se refiera al 'número del empleado', pero al no poder tener una certeza de ella, considero que es mejor eliminar la columna.
    # - 'date(list)': Hemos creado esta columna únicamente para extraer el mes y el año de cada fecha, así que tras esto, la podemos borrar del dataframe
    # - 'date': Tras desdoblar esta columna en año y mes, y a priori, no estar interesados en el día exacto, podemos borrarla también
df_clientes2.drop(columns = ['latitude', 'longitude', 'nr.employed', 'date(list)', 'date'], inplace = True)

#Por último, hacemos ajustes puntuales a los formatos y tipos del resto de columnas, con el objetivo de preservar la homogeneidad y facilitar futuras operaciones
#COLUMNA 'contact'
df_clientes2['contact'] = df_clientes2['contact'].str.title()

#COLUMNA 'poutcome'
df_clientes2['poutcome'] = df_clientes2['poutcome'].str.title()

#COLUMNA 'y'
df_clientes2['y'] = df_clientes2['y'].str.title()

#COLUMNA 'cons.conf.idx'
df_clientes2['cons.conf.idx'] = df_clientes2['cons.conf.idx'].str.replace(',','.').str.replace('"','')
df_clientes2['cons.conf.idx'] = pd.to_numeric(df_clientes2['cons.conf.idx'])
df_clientes2['cons.conf.idx'] = df_clientes2['cons.conf.idx'].astype("float64")

#Hacemos un print final en este bloque de las primeras 20 columns, de la información y del recuento de null de las columnas,
# para comprobar que lo hemos hecho correctamente
print(df_clientes2.head(10))
print(df_clientes2.isnull().sum())
print(df_clientes2.isna().sum())
print(df_clientes2.info())


#GUARDADO DE ESTADÍSTICAS DESCRIPTIVAS EN ARCHIVO .CSV
#En los próximos pasos, las variables numéricas, especialmente las continuas, serán organizadas en grupos, lo que ayudará a su representación en gráficas.
#Por motivos de limpieza y homogeneidad, esas columnas serán borradas del dataframe, ya que no trabajaremos con ellos. Debido a ello, en este paso voy a
#extraer las estadísticas descriptivas de todas esas columnas, y tras esto, guardarlas en un archivo .csv.
descripcion_principal = df_clientes2[['duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx','cons.conf.idx']].describe()
print(descripcion_principal)
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL', exist_ok = True)
descripcion_principal.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/descriptive_statistics_main.csv')


#CREACIÓN DE COLUMNAS NUEVAS MEDIANTE FUNCIONES Y FORMATEO DE DATOS
#Vamos a crear columnas nuevas para poder agrupar más fácilmente en función de ciertos tipos de datos:
#COLUMNA NUEVA - 'Age group': Vamos a crear una columna que clasifique los diferentes rangos de edades en grupos categoricos
edad_maxima = df_clientes2['age'].max()
def clasificacion_edades(edad):
    if edad == 0:
        return 'Not informed'
    elif 0 < edad <= 30:
        return 'Young [0 - 30]'
    elif 30 < edad <= 55:
        return 'Adult [30 - 55]'
    elif 55 < edad <= edad_maxima:
        return 'Elder [> 55]'
df_clientes2['Age group']= df_clientes2['age'].apply(clasificacion_edades)

#COLUMNA NUEVA - 'Job group': Vamos a crear una columna que clasifique los diferentes tipos de empleo en grupos categoricos
tipos_empleo = df_clientes2['job'].unique()
print(tipos_empleo)
def clasificacion_empleo(empleo):
    if empleo in ['Self-employed','Entrepreneur']:
        return 'Employer'
    elif empleo == 'Retired':
        return 'Retired'
    elif empleo == 'Unemployed':
        return 'Unemployed'
    elif empleo == 'Not Informed':
        return 'Not informed'
    else:
        return 'Employee'
df_clientes2['Job group']= df_clientes2['job'].apply(clasificacion_empleo)

#COLUMNA NUEVA - 'Educational group': Vamos a crear una columna que clasifique los diferentes tipos de empleo en grupos categoricos
tipos_educacion = df_clientes2['education'].unique()
print(tipos_educacion)
def clasificacion_educacion(educacion):
    if educacion in ['basic.4y, basic.6y, basic.9y']:
        return 'Basic education'
    elif educacion == 'high.school':
        return 'High school'
    elif educacion == 'professional.course':
        return 'Professional course'
    elif educacion == 'university.degree':
        return 'University'
    elif educacion == 'Not informed':
        return 'Not informed'
    else:
        return 'Illiterate'
df_clientes2['Educational group']= df_clientes2['education'].apply(clasificacion_educacion)
#Esta organización resulta más cómoda e intuitiva que la anterior, así que podemos borrar la columna 'education' sin miedo a perder información
df_clientes2.drop(columns = ['education'], inplace = True)

#COLUMNA NUEVA - 'Last call (minutes)': Vamos a crear una columna que clasifique el tiempo que duró la última llamada que se realizó al cliente
print(df_clientes2['duration'].describe())
#Como podemos ver por el valor mínimo y máximo, la llamada más corta duró 0 segundos, y la más larga 4918 segundos. La media es de 257.77 segundos,
#y la desviación estándar de 258.77 segundos. Segùn los valores de los cuartiles, el 75% de las llamadas se encuentran entre los 0 y los 319 segundos
#Sabiendo esto, vamos a definir los grupos en función del rango de minutos que duró la llamada:
def duracion_llamada(minutos):
    if 0 <= minutos <= 5:
        return '0-5 minutes'
    elif 5 < minutos <= 15:
        return '5-15 minutes'
    elif 15 < minutos <= 30:
        return '15-30 minutes'
    else:
        return '+30 minutes'
df_clientes2['Last call (range)']= df_clientes2['duration'].apply(duracion_llamada)

#COLUMNA NUEVA - '#Contacts during campaign': Vamos a crear una columna que clasifique los datos según las veces que se contactó al cliente durante la campaña
print(df_clientes2['campaign'].describe())
# #Como podemos ver por el valor mínimo y máximo, el número mínimo de veces contactadas es 1, y el máximo son 56. La media son 2.56 veces, y la desviación estándar
# son 2.77 veces. Segùn los valores de los cuartiles, para el 25% de los usuarios se contactó 1 vez, y para el 75% de los usuarios se contactó entre 1 y 3 veces.
# #Sabiendo esto, vamos a definir los grupos en función del rango de veces que se contactó:
def veces_contacto(vez):
    if 1 <= vez <= 5:
        return '1-5 contacts'
    elif 5 < vez <= 10:
        return '5-10 contacts'
    elif vez > 10:
        return '+10 contacts'
df_clientes2['Contacts during campaign (range)']= df_clientes2['campaign'].apply(veces_contacto)

#COLUMNA NUEVA - 'Days from last call': Vamos a crear una columna que clasifique hace cuántos días se realizó el último contacto con el cliente.
print(df_clientes2['pdays'].describe())
#Como podemos ver por el valor mínimo y máximo, el mínimo de días desde el último contacto son 0, y el máximo son 999 días. La media es de 962.37 días,
#y la desviación estándar de 187.15 días. Segùn los valores de los cuartiles, el 75% de los últimos contactos se encuentran entre los 0 y los 999 días.
# Necesitamos más información, así que vamos a hacer un value_counts():
distrib_ultima_llamada = df_clientes['pdays'].value_counts()
print(distrib_ultima_llamada)
#Como podemos ver, de las 42,752 entradas que disponemos tras la limpieza de datos, en 41412 de ellas, la última llamada se realizó hace 999 días. La información
#que nos aporta esta distribución es escasa, ya que un valor está presente en el ~97% de las entradas. No obstante, en vez de borrar esta columna, vamos a dividir
#los datos entre aquellos que recibieron el último contacto hace 999 días (lo que presumiblemente significa que se recibió antes de disponer de registros o algo
#similar, pero no podemos asegurarlo), y aquellos que lo recibieron hace cualquier otro número de días.
def ultima_llamada(dia):
    if 0 <= dia <= 27:
        return '0-27 days'
    else:
        return '999 days'
df_clientes2['Days from last call (range)']= df_clientes2['pdays'].apply(ultima_llamada)

#COLUMNA NUEVA - 'IPC level': Vamos a crear una columna que clasifique los niveles de IPC en base a los datos aportados en la columna 'cons.price.idx'.
print(df_clientes2['cons.price.idx'].describe())
# Observando la distribución de los datos, y poniendo especial atención a la media y los cuartiles, podemos dividir el IPC (es decir, el nivel general de los precios
# en cada momento) en tres rangos diferentes, que calificaremos como 'low', 'intermediate' y 'high', en referencia a dichos precios. Los rangos irán marcados por el
# mínimo, el cuartil 1, el cuartil 3 y el máximo
ipc_minimo = df_clientes2['cons.price.idx'].min()
q1_ipc = df_clientes2['cons.price.idx'].quantile(0.25) #Sacamos el valor que determina el Q1
q3_ipc = df_clientes2['cons.price.idx'].quantile(0.75) #Sacamos el valor que determina el Q3
print(ipc_minimo)
print(q1_ipc)
print(q3_ipc)
def niveles_ipc(ipc):
    if ipc_minimo <= ipc <= q1_ipc:
        return 'Low IPC [92.201 - 93.075]'
    elif q1_ipc < ipc <= q3_ipc:
        return 'Medium IPC [93.075 - 93.994]'
    else:
        return 'High IPC [< 93.994]'
df_clientes2['IPC (range)']= df_clientes2['cons.price.idx'].apply(niveles_ipc)

#COLUMNA NUEVA - 'Confidence level': Vamos a crear una columna que clasifique la confianza del consumidor en cada momento,  en base a los datos aportados
# en la columna 'cons.price.idx'.
print(df_clientes2['cons.conf.idx'].describe())
# Observando la distribución de los datos, y poniendo especial atención a la media y los cuartiles, podemos dividir la confianza (es decir, el nivel de confianza de
# los consumidores en cada momento, y por tanto su predisposición a asumir riesgos) en tres rangos diferentes, que calificaremos como 'low', 'intermediate' y 'high',
# Los rangos irán marcados por el mínimo, el cuartil 1, el cuartil 3 y el máximo
confi_minimo = df_clientes2['cons.conf.idx'].min()
q1_confi = df_clientes2['cons.conf.idx'].quantile(0.25) #Sacamos el valor que determina el Q1
q3_confi = df_clientes2['cons.conf.idx'].quantile(0.75) #Sacamos el valor que determina el Q3
print(confi_minimo)
print(q1_confi)
print(q3_confi)
def niveles_confi(confianza):
    if confi_minimo <= confianza <= q1_confi:
        return 'Low confidence [(-50.8) - (-42.7)]'
    elif q1_confi < confianza <= q3_confi:
        return 'Medium confidence [(-42.7) - (-36.4)]'
    else:
        return 'High confidence [> (-36.4)]'
df_clientes2['Confidence level (range)']= df_clientes2['cons.conf.idx'].apply(niveles_confi)

#COLUMNA NUEVA - 'Employment variation': Vamos a crear una columna que clasifique la tasa de variabilidad del empleo  en cada momento,  en base a los datos aportados
# en la columna 'emp.var.rate'.
print(df_clientes2['emp.var.rate'].describe())
# Observando la distribución de los datos, y poniendo especial atención a la media y los cuartiles, podemos dividir la tasa de variabilidad del empleo (es decir, si
# empleo crece, disminuye o estable en cada momento) en tres rangos diferentes: 'Growth', 'Stability', 'Reduction'
# Los rangos irán marcados por valores negativos (Reduction), valores cercanos a 0 (Stability) y valores positivos (Growth)
empleo_max = df_clientes2['emp.var.rate'].max() #Sacamos el valor máximo
empleo_min = df_clientes2['emp.var.rate'].min() #Sacamos el valor mínimo
def variabilidad_empleo(variabilidad):
    if empleo_min <= variabilidad < (-0.1):
        return 'Reduction [< (-0.1)]'
    elif (-0.1) <= variabilidad <= 0.1:
        return 'Stability'
    elif 0.1 < variabilidad <= empleo_max:
        return 'Growth [< 0.1]'
df_clientes2['Employment variation (range)']= df_clientes2['emp.var.rate'].apply(variabilidad_empleo)

#COLUMNA MODIFICADA - 'contract_month'
#Considerando que toda nuestra información está en inglés, vamos a escribir una función
def transformar_meses(mes):
    if mes == 'Enero':
        return 'January'
    if mes == 'Febrero':
        return 'February'
    if mes == 'Marzo':
        return 'March'
    if mes == 'Abril':
        return 'April'
    if mes == 'Mayo':
        return 'May'
    if mes == 'Junio':
        return 'June'
    if mes == 'Julio':
        return 'July'
    if mes == 'Agosto':
        return 'August'
    if mes == 'Septiembre':
        return 'September'
    if mes == 'Octubre':
        return 'October'
    if mes == 'Noviembre':
        return 'November'
    if mes == 'Diciembre':
        return 'December'
    else:
        return 'No informado' #No deberían quedar valores null, pero lo establecemos como mecanismo defensivo por si acaso.
df_clientes2['contact_month']= df_clientes2['contact_month'].apply(transformar_meses)

#CAMBIOS DE NOMBRE Y ORDEN DE COLUMNAS
#Para finalizar con el EDA y poder realizar visualizaciones de nuestros datos de manera correcta e intuitiva, vamos a realizar unos últimos ajustes en nuestro
#dataframe, en relación al nombre y al orden de nuestras columnas
df_clientes2.rename(columns = {'age': 'Age (number)',
                               'job': 'Job',
                               'marital': 'Marital status',
                               'housing': 'Mortgage (Yes/No)',
                               'loan': 'Other loans (Yes/No)',
                               'contact': 'Contact method',
                               'poutcome': 'Prev. marketing campaign',
                               'previous': '#Contacts before campaign',
                               'id_': 'Client ID',
                               'pdays': 'Days from last call',
                               'cons.conf.idx': 'Confidence level',
                               'cons.price.idx': 'IPC',
                               'emp.var.rate': 'Employment variation',
                               'campaign': '#Contacts during campaign',
                               'duration': 'Last call (minutes)',
                               'contact_year': 'Contact date (year)',
                               'contact_month': 'Contact date (month)',
                               'y': 'Objective variable'
                               }, inplace = True)
df_clientes2 = df_clientes2[['Age (number)', 'Age group', 'Job', 'Job group', 'Educational group', 'Marital status', 'Contact method', 'Mortgage (Yes/No)',
                            'Other loans (Yes/No)', 'Prev. marketing campaign','#Contacts before campaign','Last call (minutes)', 'Last call (range)',
                            'Days from last call','Days from last call (range)','#Contacts during campaign','Contacts during campaign (range)',
                            'Contact date (year)', 'Contact date (month)', 'IPC', 'IPC (range)','Confidence level', 'Confidence level (range)',
                            'Employment variation', 'Employment variation (range)', 'Objective variable', 'Client ID']]
#Realizamos un print para comprobar que los datos han sido introducidos correctamente, y por tanto los cambios se han producido con éxito
print(df_clientes2.head(10))

#Por último, y como medida cautelar final, realizamos una breve prueba para comprobar si, después de todos los pasos de limpieza y exploración realizados,
#hubies algún dato duplicado en nuestro dataframe
duplicates =df_clientes2[df_clientes2.duplicated()]
print(duplicates)
#El print nos devuelve 'Empty DataFrame', con lo que nos aseguramos de que no hay datos duplicados

#GUARDADO DE LA TABLA LIMPIA EN .CSV
#Una vez hemos terminado el EDA de nuestra tabla principal, guardamos los datos en formato .csv. Esto nos permitirá importar este .csv de nuevo como un dataframe
#en un nuevo archivo .py, que estará destinado a realizar el merge con la tabla auxiliar, y en otro destinado a llevar a cabo las diferentes visualizaciones de los datos.
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL', exist_ok = True)
df_clientes2.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/01_EDA_bank_additional.csv')




