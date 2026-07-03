# MODULE-8-PYTHON-DATA-LIFECYCLE

Repositorio correspondiente al proyecto final del **Módulo 8: Python for Data Analysis** del programa **Data & Analytics V3 de ThePower**, desarrollado por **Miguel Encinas**.

Este proyecto se centra en la aplicación de Python para realizar la limpieza y representación de un conjunto de datos real relacionado con una campaña de marketing bancario. Para ello, se ha realizado un flujo de trabajo que incluye **carga de datos, limpieza, transformación, unión de diferentes dataframes, análisis exploratorio, visualización de datos y una primera aproximación a la predicción de la variable objetivo**.

El objetivo principal del proyecto ha sido estudiar las características de los clientes, analizar qué factores pueden estar relacionados con la contratación del producto o servicio ofrecido durante la campaña, y representar ambos análisis con diferentes técnicas de visualización, mediante los paquetes matplotlib y seaborn. Además, se ha explorado si los datos tratados pueden tener cierto valor predictivo mediante un par modelos sencillos de aprendizaje supervisado.

## ⬇️ Carga de los datos
El proyecto parte de dos fuentes principales de datos, ambas incluidas en la carpeta 'Project Data/Raw Data':
- **bank-additional.csv**: tabla principal del proyecto. Contiene información de clientes contactados durante una campaña de marketing bancario, así como su información demográfica, información de contacto, datos de campañas previas, indicadores macroeconómicos y la variable objetivo.
- **customer-details.xlsx**: archivo auxiliar en formato Excel, dividido en varias hojas correspondientes a diferentes años en los que el cliente se registró en el banco. Este archivo contiene información adicional de los clientes, como ingresos, número de hijos o adolescentes en casa, fecha de alta y frecuencia de visitas a la página web.

A partir de dichos archivos se generaron diferentes archivos tratados, disponibles en la carpeta Project Data/Curated data'.

## ✨ Limpieza y transformación de los datos
La limpieza de datos se realizó principalmente en los scripts '01_EDA_bank_additional.py' y '02_EDA_customer_details.py', incluidos en la carpeta 'Notebooks (py)'.

En primer lugar, se trabajó con el archivo **bank-additional.csv**, revisando la estructura general del dataframe, los tipos de datos, los valores nulos y la coherencia  de las columnas. A partir de esta revisión se aplicaron diferentes decisiones de limpieza y transformación:
- Sustitución de valores nulos por categorías como **Not informed** cuando se consideró importante conservar las filas.
- Sustitución puntual de valores nulos por el valor más frecuente cuando la distribución de la variable lo justificaba.
- Eliminación de columnas con escaso valor analítico o con interpretación dudosa, como 'default', 'latitude', 'longitude', 'nr.employed' y 'euribor3m'.
- Conversión de variables numéricas almacenadas como texto, especialmente aquellas con separadores decimales o comillas.
- Extracción del mes y el año de contacto a partir de la columna de fecha.
- Eliminación de registros sin fecha de contacto, ya que esta información era relevante para el análisis temporal realizado posteriormente.

Además, se crearon nuevas variables categóricas para mejorar la interpretación de los datos:
- **Age group**
- **Job group**
- **Educational group**
- **Last call (range)**
- **Contacts during campaign (range)**
- **Days from last call (range)**
- **IPC (range)**
- **Confidence level (range)**
- **Employment variation (range)**

De manera similar, en el archivo **customer-details.xlsx** se unieron las hojas correspondientes a los años 2012, 2013 y 2014 (mediante el método .concat()), se comprobaron los nombres de las columnas y se concatenaron los datos en un único dataframe. A continuación, se realizaron transformaciones adicionales sobre variables como los ingresos, la frecuencia mensual de visitas web y la fecha de registro del cliente (estas transformaciones están relacionadas con las recién descritas).

## ↔️ Unión de tablas
Una vez tratadas la tabla principal y la tabla auxiliar, se realizó la unión de ambas mediante el script '03_merge_dataframes.py'.

La unión se llevó a cabo con el método **merge()**, a través la columna **Client ID**, la cual figuraba en ambos dataframes. El resultado final se guardó como:

- **03_merge_dataframes.csv** - Fichero de datos en formato .csv.
- **03_DF_Final_Excel.xlsx** - Datos transformados a archivo Excel, con la opción 'Filtro' aplicada a todas las columnas.

Estos archivos constituyen la versión final del conjunto de datos tratado, sobre la que se realizaron las visualizaciones y la prueba de los modelados predictivos.

## 🔎 Visualización de los datos
Tras la limpieza y unión de los datos, se generaron diferentes visualizaciones mediante el script '04_data_visualizations.py'.

Las visualizaciones se organizaron en tres grandes bloques:

### 1. Distribución general de clientes
En este bloque se estudió cómo se distribuyen los clientes en función de diferentes variables categóricas, como son la edad, grupo profesional, nivel educativo, estado civil, campañas previas, duración de la última llamada o variable objetivo.

Estas visualizaciones me permitieron entender la composición general del conjunto de datos, antes de analizar la relación de cada variable con la contratación del producto (variable objetivo).

### 2. Distribución de la variable objetivo
En este segundo bloque se analiza cómo varía la proporción de clientes que se suscribieron o noa un servicio/producto, en función de diferentes características del conjunto de datos.

Por ello, se estudió la relación entre la variable objetivo y diferentes variables:

- Grupo de edad.
- Grupo profesional.
- Nivel educativo.
- Estado civil.
- Préstamo hipotecario.
- Otros préstamos.
- Resultado de campañas previas.
- Número de contactos antes y durante la campaña.
- Duración de la última llamada.
- Año de contacto.
- IPC.
- Nivel de confianza del consumidor.
- Tasa de variación del empleo.
- Ingresos anuales.
- Número de hijos o adolescentes en casa.
- Frecuencia de visitas web.

### 3. Evolución temporal
Por último, se generó una visualización orientada a estudiar el porcentaje de suscripciones y no suscripciones a productos/servicios a lo largo del tiempo, en relación con el año de contacto con el cliente. Se mostró además un ejemplo de este tipo de gráfico aplicado a diferentes valores de una variable, comparando el porcentaje de clientes que se suscribió a un producto/servicio cuando su última llamada duró 0-5 minutos, con los clientes cuya última llamada duró 15-30 minutos.

## 🔮 Predicción de la variable objetivo
Como parte final del proyecto, se realizó una primera aproximación a la predicción de la variable objetivo mediante el script 05_objective_variable_prediction.py'.

Para ello, se aplicó un flujo básico de Machine Learning con **scikit-learn**, siguiendo los siguientes pasos:

1. Eliminación de columnas redundantes o poco útiles para el modelo (p. ej., las columnas que habia creado previamente para clasificar variables numéricas en categorías).
2. Transformación de la variable objetivo a formato binario (No = 0, Yes = 1).
3. Separación de los datos en conjunto de entrenamiento y conjunto de testeo.
4. Uso de 'train_test_split' con 'stratify', para reflejar el desbalance que existe en las respuestas de la variable objetivo.
5. Escalado de variables numéricas (int64 y float64) mediante 'StandardScaler'.
6. Codificación de variables categóricas mediante 'OneHotEncoder'.
7. Entrenamiento de un modelo de **Regresión Logística**.
8. Comparación con un modelo de **Árbol de Decisión**.
9. Evaluación de ambos modelos mediante los parámetros de 'accuracy', 'precision' y una matriz de confusión.

La regresión logística mostró una buena accuracy general, pero una precision más limitada, especialmente por la dificultad para predecir correctamente los casos positivos. En este sentido, el árbol de decisión mejoró notablemente la precision y mantuvo una accuracy elevada, lo que indica que el conjunto de datos podría tener cierto potencial predictivo, aunque sería necesario profundizar en el perfeccionamiento del modelo predictivo, especialmente en el ajuste de parámetros.

## ℹ️ Información de interés
**Notebooks (py)**: Carpeta que contiene los scripts de Python utilizados durante el proyecto.
- **01_EDA_bank_additional.py**: Limpieza, transformación y análisis exploratorio inicial de la tabla principal.
- **02_EDA_customer_details.py**: Limpieza y transformación del archivo auxiliar de clientes.
- **03_merge_dataframes.py**: Unión de la tabla principal y la tabla auxiliar a través de la columna 'Client ID'.
- **04_data_visualizations.py**: Creación de visualizaciones para estudiar la distribución de clientes, la variable objetivo y la evolución temporal.
- **05_objective_variable_prediction.py**: Primera aproximación a la predicción de la variable objetivo mediante modelos de Machine Learning.

**Project Data/Raw Data**: Carpeta que contiene los datos originales (crudos) del proyecto.
- **bank-additional.csv**: Archivo principal original.
- **customer-details.xlsx**: Archivo auxiliar original con información adicional de clientes.

**Project Data/Curated data**: Carpeta que contiene los archivos generados tras la limpieza, transformación y unión de datos.
- **01_EDA_bank_additional.csv**
- **01_descriptive_statistics_main.csv**
- **02_EDA_customer_details.csv**
- **02_descriptive_statistics_details.csv**
- **03_merge_dataframes.csv**
- **03_DF_Final_Excel.xlsx**

**Visualizations**: Carpeta que contiene las visualizaciones generadas durante el análisis, organizadas en diferentes subcarpetas.

## 🛠️ Herramientas y lenguajes utilizados
- Lenguaje: **Python**
- Entorno: **Visual Studio Code**
- Librerías principales:
  - **pandas**
  - **NumPy**
  - **matplotlib**
  - **seaborn**
  - **scikit-learn**

⚠️ Los scripts contienen **rutas locales absolutas**, por lo que para ejecutar el proyecto en otro ordenador sería necesario **adaptar dichas rutas** a la estructura local del nuevo equipo.\
\
⚠️ Para la elaboración del código, **no se usaron herramientas de IA generativa**, el código fue generado de manera íntegra por el usuario.\
\
⚠️ En ocasiones puntuales, **se utilizó inteligencia artificial como asistente** (sin generación directa de código) para enocontrar el fallo en un código que el usuario no fue capaz de encontrar por sí mismo.\
\
⚠️ Las herramientas de auto-completado de código, como la extensión 'auto​Docstring', **fueron desactivadas para este ejercicio**, favoreciendo la generación de código original por parte del usuario.

## ↪️ Conclusiones
En general, este proyecto me ha permitido:
- Trabajar con un flujo completo de análisis de datos usando **Python** en el entorno de **Visual Studio Code**.
- Cargar, limpiar, transformar y unir datos procedentes de archivos **csv** y **Excel**.
- Aplicar diferentes razonamientos para tratar valores nulos, columnas redundantes y variables con formatos poco adecuados, **analizando el conjunto de datos en general**.
- Crear nuevas **variables categóricas** para facilitar el análisis y la visualización de los datos.
- Generar **visualizaciones** orientadas a estudiar tanto la distribución general de los clientes como la relación de diferentes variables con la variable objetivo.
- Realizar una primera aproximación a modelos predictivos mediante **scikit-learn**.
- En general, **comprender el ciclo de vida completo del dato** y aplicar un flujo de trabajo extrapolable a un caso real.
