# MODULE-8-PYTHON-DATA-LIFECYCLE
# MODULE-8-PYTHON-DATA-LIFECYCLE

Repositorio correspondiente al proyecto final del **Módulo 8: Python for Data Analysis** del programa **Data & Analytics V3 de ThePower**, desarrollado por **Miguel Encinas**.

Este proyecto se centra en la aplicación de Python para realizar la limpieza y representación de un conjunto de datos real relacionado con una campaña de marketing bancario. Para ello, se ha realizado un flujo de trabajo que incluye **carga de datos, limpieza, transformación, unión de diferentes dataframes, análisis exploratorio, visualización de datos y una primera aproximación a la predicción de la variable objetivo**.

El objetivo principal del proyecto ha sido estudiar las características de los clientes, analizar qué factores pueden estar relacionados con la contratación del producto o servicio ofrecido durante la campaña, y representar ambos análisis con diferentes técnicas de visualización, mediante los paquetes matplotlib y seaborn. Además, se ha explorado si los datos tratados pueden tener cierto valor predictivo mediante un par modelos sencillos de aprendizaje supervisado.

## ⬇️ Carga de los datos

El proyecto parte de dos fuentes principales de datos, ambas incluidas en la carpeta 'Project Data/Raw Data':
- **bank-additional.csv**: tabla principal del proyecto. Contiene información de clientes contactados durante una campaña de marketing bancario, así como su información demográfica, información de contacto, datos de campañas previas, indicadores macroeconómicos y la variable objetivo.
- **customer-details.xlsx**: archivo auxiliar en formato Excel, dividido en varias hojas correspondientes a diferentes años en los que el cliente se registró en el banco. Este archivo contiene información adicional de los clientes, como ingresos, número de hijos o adolescentes en casa, fecha de alta y frecuencia de visitas a la página web.

A partir de estos archivos se generaron diferentes archivos tratados, disponibles en la carpeta Project Data/Curated data'.

## Limpieza y transformación de los datos

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

## Unión de tablas

Una vez tratadas la tabla principal y la tabla auxiliar, se realizó la unión de ambas mediante el script `03_merge_dataframes.py`.

La unión se llevó a cabo mediante la columna **Client ID**, común a ambos dataframes. El resultado final se guardó como:

- **03_merge_dataframes.csv**
- **03_DF_Final_Excel.xlsx**

Estos archivos constituyen la versión final del dataset tratado, sobre la que se realizaron las visualizaciones y la prueba de modelado predictivo.

## Visualización de los datos

Tras la limpieza y unión de los datos, se generaron diferentes visualizaciones mediante el script `04_data_visualizations.py`.

Las visualizaciones se organizaron en tres grandes bloques:

### 1. Distribución general de clientes

En este bloque se estudia cómo se distribuyen los clientes en función de diferentes variables categóricas, como edad, grupo profesional, nivel educativo, estado civil, préstamos, campañas previas, año de contacto, duración de la última llamada o variable objetivo.

Estas visualizaciones permiten entender la composición general del dataset antes de analizar la relación de cada variable con la contratación del producto.

### 2. Distribución de la variable objetivo

En este segundo bloque se analiza cómo varía la proporción de clientes que aceptaron o no aceptaron la oferta en función de diferentes características.

Entre otras variables, se estudia la relación entre la variable objetivo y:

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

Por último, se generaron visualizaciones orientadas a estudiar la evolución de ciertas variables a lo largo del tiempo, especialmente en relación con el año de contacto y el comportamiento de la variable objetivo.

## Predicción de la variable objetivo

Como parte final del proyecto, se realizó una primera aproximación a la predicción de la variable objetivo mediante el script `05_objective_variable_prediction.py`.

Para ello, se aplicó un flujo básico de Machine Learning con **scikit-learn**, siguiendo los siguientes pasos:

1. Eliminación de columnas redundantes o poco útiles para el modelo.
2. Transformación de la variable objetivo a formato binario.
3. Separación de los datos en conjunto de entrenamiento y conjunto de testeo.
4. Uso de `train_test_split` con `stratify`, para respetar el desbalanceo existente en la variable objetivo.
5. Escalado de variables numéricas mediante `StandardScaler`.
6. Codificación de variables categóricas mediante `OneHotEncoder`.
7. Entrenamiento de un modelo de **Regresión Logística**.
8. Comparación con un modelo de **Árbol de Decisión**.
9. Evaluación mediante accuracy, precision y matriz de confusión.

La regresión logística mostró una buena accuracy general, pero una precision más limitada, especialmente por la dificultad para predecir correctamente los casos positivos. Posteriormente, el árbol de decisión mejoró la precision y mantuvo una accuracy elevada, lo que sugiere que el dataset puede tener cierto potencial predictivo, aunque sería necesario profundizar con técnicas adicionales de validación, ajuste de hiperparámetros y tratamiento del desbalanceo.

## ℹ️ Información de interés

**Notebooks (py)**: Carpeta que contiene los scripts de Python utilizados durante el proyecto.

- **01_EDA_bank_additional.py**: limpieza, transformación y análisis exploratorio inicial de la tabla principal.
- **02_EDA_customer_details.py**: limpieza y transformación del archivo auxiliar de clientes.
- **03_merge_dataframes.py**: unión de la tabla principal y la tabla auxiliar mediante `Client ID`.
- **04_data_visualizations.py**: creación de visualizaciones para estudiar la distribución de clientes, la variable objetivo y la evolución temporal.
- **05_objective_variable_prediction.py**: primera aproximación a la predicción de la variable objetivo mediante modelos de Machine Learning.

**Project Data/Raw Data**: Carpeta que contiene los datos originales del proyecto.

- **bank-additional.csv**: archivo principal original.
- **customer-details.xlsx**: archivo auxiliar original con información adicional de clientes.

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
  - **openpyxl**
  - **scikit-learn**

## ▶️ Ejecución del proyecto

Para ejecutar este proyecto en otro equipo, es recomendable clonar el repositorio e instalar las dependencias principales:

```bash
git clone https://github.com/therealmike10/MODULE-8-PYTHON-DATA-LIFECYCLE.git
cd MODULE-8-PYTHON-DATA-LIFECYCLE
pip install pandas numpy matplotlib seaborn openpyxl scikit-learn
```

Después, se pueden ejecutar los scripts de Python siguiendo el orden lógico del proyecto:

```bash
python "Notebooks (py)/01_EDA_bank_additional.py"
python "Notebooks (py)/02_EDA_customer_details.py"
python "Notebooks (py)/03_merge_dataframes.py"
python "Notebooks (py)/04_data_visualizations.py"
python "Notebooks (py)/05_objective_variable_prediction.py"
```

⚠️ **Nota importante**: los scripts contienen rutas locales absolutas, por lo que para ejecutar el proyecto en otro ordenador sería necesario adaptar dichas rutas a la estructura local del nuevo equipo o convertirlas en rutas relativas al repositorio.

## ↪️ Conclusiones

En general, este proyecto me ha permitido:

- Trabajar con un flujo completo de análisis de datos usando **Python**.
- Cargar, limpiar, transformar y unir datos procedentes de archivos **CSV** y **Excel**.
- Aplicar criterios razonados para tratar valores nulos, columnas redundantes y variables con formatos poco adecuados.
- Crear nuevas variables categóricas para facilitar el análisis y la visualización de los datos.
- Generar visualizaciones orientadas a estudiar tanto la distribución general de los clientes como la relación de diferentes variables con la variable objetivo.
- Realizar una primera aproximación a modelos predictivos mediante **scikit-learn**.
- Comprender la importancia del preprocesamiento, la separación entre entrenamiento y testeo, el escalado de variables, la codificación de categorías y la evaluación del rendimiento del modelo.

Este proyecto supone una integración de varias fases fundamentales del ciclo de vida del dato: desde la obtención y preparación de la información hasta su análisis, visualización e interpretación final.

## 🔎 Posibles mejoras futuras

Algunas mejoras que podrían añadirse en futuras versiones del proyecto son:

- Sustituir las rutas absolutas por rutas relativas para mejorar la reproducibilidad.
- Añadir un archivo `requirements.txt` con las librerías necesarias.
- Modularizar parte del código en funciones reutilizables.
- Guardar automáticamente las visualizaciones generadas desde el script correspondiente.
- Añadir métricas adicionales para la evaluación del modelo, como recall, F1-score, ROC-AUC o balanced accuracy.
- Aplicar técnicas específicas para tratar el desbalanceo de la variable objetivo.
- Probar modelos adicionales, como Random Forest, Gradient Boosting o XGBoost.
- Añadir validación cruzada y búsqueda de hiperparámetros.
- Crear un dashboard final en Power BI, Tableau o Streamlit para facilitar la exploración interactiva de los resultados.
