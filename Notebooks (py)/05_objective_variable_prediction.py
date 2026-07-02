import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl
import os


#3. PREDICCIÓN DE LA VARIABLE OBJETIVO ('y'): Como comentaba en el inicio del primer documento, previamente realicé el curso
#'IBM Tools for Data Science'. Por tanto, a pesar de que en este curso no hemos profundizado en ese aspecto, creo que este dataset
#es una buena oportunidad para aplicar la parte de Data Science que había trabajado previamente. Por ello, he usado el paquete
#scikit-learn para intentar determinar el valor predictivo del dataframe del que disponemos, es decir, estudiar su potencial para
#predecir el valor de la 'Objective variable'. Puede que el workflow presente algún fallo, ya que la parte de Data Science no la he
#trabajado tan ampliamente como la parte de Data Analysis, pero me parecía una buena oportunidad para practicar.

#Vamos a aplicar,por tanto, un flujo de trabajo para desarrollar un modelo de regresión logística a nuestros datos.el modelo de regresión
#logística es un modelo de aprendizaje supervisado, es decir, nosotros le damos categorías 'etiquetadas' para que aprendan a partir de ellos
#y puedan aplicar ese conocimiento sobre datos nuevos, permitiéndoles predecir sus etiquetas.

#IMPORTACIÓN DE NUESTRO DATAFRAME
pd.set_option('display.max_columns', None)
file1 = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/8. PYTHON FOR DATA/PROYECTO_FINAL/03_merge_dataframes.csv"
df_final = pd.read_csv(file1, index_col = 0)
# print(df_final.head(10))

#IMPORTACIÓN DE MÓDULOS A PARTIR DE SCIKIT-LEARN
#Comenzamos importando los módulos necesarios de scikit-learn
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, precision_score, accuracy_score, ConfusionMatrixDisplay
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

    #1. En primer lugar, vamos a eliminar varias columnas del dataframe a tratar: La columna Client ID, ya que no aporta a la predicción y procesarla tendría un
    #coste computacional altísimo y sin sentido. Otras columnas que vamos a usar son las categóricas que he creado en la limpieza de datos, ya que al final, a
    #la hora de usar un modelo de predicción, es información redundante que ya se puede obtener de sus columnas float64 correspondientes
df_final = df_final.drop(columns = ['Age group','Job group','Contact date (month)', 'Last call (range)', 'Days from last call (range)',
                                    'Contacts during campaign (range)', 'IPC (range)', 'Confidence level (range)','Employment variation (range)',
                                    'Client ID', 'Annual income (range)', 'Web visit freq. (per month)' ])
        #Variable objetivo: Transformamos nuestra variable objetivo nuevamente en binaria, sustituyendo 'Yes' y 'No' por 0 y 1
df_final['Objective variable'] = df_final['Objective variable'].replace('No', 0).replace('Yes', 1)

    #2.Separación de los datos del modelo: Antes de realizar el pre-procesamiento, separamos los datos en aquellos que van a ser usados para el entrenamiento
    #del modelo, y aquellos que van a ser usados para su testeo. Realizar este paso antes del pre-procesamiento evita el filtrado de datos o 'data-leakage',
    #de manera que nos aseguramos de que el modelo 'no vea los datos de testeo' antes de poner a prueba el modelo
X = df_final.drop(['Objective variable'], axis = 1)
y = df_final['Objective variable']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 27, stratify = y) #Dividimos los datos en dos subconjuntos. El conjunto de
#entrenamiento (X_train, y_train), que nos servirá para entrenar a nuestro modelo, y el subconjunto de testeo (X_test, y_test), que nos servirá para aplicar
#el entrenamiento realizado previamente. El random_state se refiere a un patrón de aletoriedad que vamos a fijar, de manera que, si otra persona decide aplicar
#este método en otro equipo, pueda obtener la misma distribcuión aleatoria, haciendo por tanto que sea reproducible. Si no fijamos un test_size, el método
#train_test_split tomará el 75% de los datos para entrenamiento, y el 25% para testeo. Añadimos stratitify = y para reflejar en la división entre conjunto de testeo
# y entrenamiento el desbalanceo que hay en nuestra variable objetivo, donde casi el 90% de nuestros resultados son 'No'

    #3. Preprocesamiento de los datos: Como hemos dicho, trabajamos en primer lugar con el conjunto de entrenamiento.El primer paso a seguir para
    #desarrollar un modelo predictivo es el pre-procesamiento de los datos,cuyo objetivo es transformar los datos para obtener una serie de variables
    #numéricas escaladas para poder usarlas como variables predictoras.Este proceso lo podemos dividir en varios pasos:
        #Columnas continuas: En primer lugar, transformamos las variables numéricas continuas de nuestro dataframe (es decir, la que sean de tipo
        #'float64'. Lo único que nos interesa de estas variables es que todas tengan el mismo peso, es decir, que estén en la misma escala. De esta
        # manera evitamos, por ejemplo, darle un mayor peso predictivo a la variable que tenga órdenes de magnitud más altos (ej: Annual income vs
        # Employment variation):
print(X_train.info()) #Antes que nada, llamamos a la info de nuestro modelo, para ver cuántas columnas tenemos de cada tipo.
continuous_columns = X_train.select_dtypes(include = ['float64','int64']).columns.tolist()#Seleccionamos las columnas de tipo 'float64' de nuestro df, y
#pasamos los títulos de dichas columnas a una lista. En este caso, añadimos las int64 también, ya que las que tenemos en este df no son binarias, y por
#tanto pueden estar en una escala diferente también, así que las añadimos por si acaso.
scaler = StandardScaler() #Invocamos el StandardScaler, herramiente de scikit_learn que nos va a permitir escalar nuestras variables
scaled_continuous = scaler.fit_transform(X_train[continuous_columns]) #Aplicamos el escalado a las columnas continuas (a modo de series) mediante .fit_transform()
scaled_df = pd.DataFrame(scaled_continuous, columns = scaler.get_feature_names_out(continuous_columns)) #Creamos un nuevo dataframe con
#nuestras nuevas variables escaladas. Reseteamos el index para que no haya problemas futuros de desalineamiento
scaled_data = pd.concat([X_train.drop(columns = continuous_columns).reset_index(drop = True), scaled_df.reset_index(drop = True)], axis = 1) #Lo unimos a
#nuestro dataset original, previamente eliminado las columnas correspondientes sin escalar. Aplicamos .reset_index() en cada uno de los dataframes para
#evitar futuros problemas de alineamiento, ya que al estar haciendo un pd.concat, si los index están desalineados, obtendríamos un error.

        #Columnas categóricas: No podemos pasar columnas categóricas por el modelo de regresión, así que es más conveniente convertirlas a variables
        #numéricas, diealmente variables binarias. Para ello, usaremos lo que se denomina como 'One Hot Encoding'. Lo que hará este método es que,
        #en vez de que nuestra variable sea 'Yes' o 'No', creará dos columnas para dicha variable, una con 'Yes' y otra con 'No', y le asignará 0 o 1
        #a cada columna, en función de si, para cada dato, la respuesta era una u otra.
categorical_columns=X_train.select_dtypes(include=['object']).columns.tolist() #Mismo planteamiento, seleccionamos las columnas tipo 'object' y pasamos
#sus títulos a una lista
ohe = OneHotEncoder(drop = 'first', sparse_output = False) #Definimos nuestro método OneHotEnconder. Usamos sparse_output = False para que no nos devuelva
# un array de SciPy. Usamos drop = 'first' para eliminar la primera categoría de las columnas creadas a partir de la variable categórica. Esto se hace
#normalmente para evitar redundancia, ya que si por ejemplo, tenemos 3 variables nuevas y dos son 0, la restante será 1; si una es 0 y otra 1, la restante
#será 0. Por tanto, con drop nos ahorramos esta redundancia de información, que puede dar problemas en nuestro modelo predictivo.
encoded_categorical = ohe.fit_transform(X_train[categorical_columns]) #Pasamos nuestra lista de columnas por el transformador de OneHotEncoder
encoded_df = pd.DataFrame(encoded_categorical, columns = ohe.get_feature_names_out(categorical_columns))
encoded_data = pd.concat([scaled_data.drop(columns = categorical_columns).reset_index(drop = True), encoded_df.reset_index(drop = True)], axis = 1)
#Unimos nuestro dataframe recién creado, con el que habíamos definido previamente tras escalar las variables continuas

        #Por último, realizamos el mismo proceso, pero con el subconjunto de testeo esta vez:
scaled_continuous1 = scaler.transform(X_test[continuous_columns]) #Aplicamos .transform() en vez de .fit_transform(), ya que no queremos que el modelo
#reaprenda con los datos de X_test, sino que simplemente, con lo que ha aprendido en los datos del X_train, transforme nuestros datos de X_test
scaled_df1 = pd.DataFrame(scaled_continuous1, columns = scaler.get_feature_names_out(continuous_columns))
scaled_data1 = pd.concat([X_test.drop(columns = continuous_columns).reset_index(drop = True), scaled_df1.reset_index(drop = True)], axis = 1)
encoded_categorical1 = ohe.transform(X_test[categorical_columns]) #Mismo razonamiento que con el StandardScaler
encoded_df1 = pd.DataFrame(encoded_categorical1, columns = ohe.get_feature_names_out(categorical_columns))
encoded_data1 = pd.concat([scaled_data1.drop(columns = categorical_columns).reset_index(drop = True), encoded_df1.reset_index(drop = True)], axis = 1)

    #5. Evaluación del modelo: Evaluamos la capacidad del modelo de regresión logística para predecir los valores correspondientes a y_test a partir de X_test
print(encoded_data.info())
print(encoded_data1.info())#Nos aseguramos de que no quedan columnas tipo 'object' en nuestros df tras el pre-procesamiento
reg_model = LogisticRegression(solver = 'saga', verbose = 1,  max_iter = 200, class_weight = 'balanced', C = 0.1) #Una vez hehco todo el preprocesamiento, creamos
#el modelo de regresión logística. En concreto, usamos el solver 'saga' (uno de los varios disponibles), con verbose = 1 le indicamos que nos vaya enseñando
#el proceso de ajuste al modelo en la zona del output, le marcamos un máximo de 200 interacciones, con class_weight = 'balanced' le indicamos que considere
#que nuestra variable objetivo está desbalanceada en cuanto a los resultados, y con C indicamos la fuerza de la regularización (más pequeño = mayor regularización)
reg_model.fit(encoded_data, y_train) #Aplicamos nuestro modelo a nuestro subconjunto de datos de entrenamiento
y_pred = reg_model.predict(encoded_data1) #Una vez calculado el modelo, lo usamos en nuestro subconjunto de testeo, para obtener una variable 'y' predicha
print(f'The accuracy of the model is {accuracy_score(y_test, y_pred)}')
print(f'The precision of the test is {precision_score(y_test, y_pred)}')
#Comparamos ambas variables, la 'y' predicha y la 'y' de entrenamiento que nos habíamos reservado desde el principio, para comparar cómo de bueno es el modelo
#en cuanto a sus predicciones, en comparación con los datos reales
print('--------------------')
cm = confusion_matrix(y_test, y_pred) #Creamos la matriz de confusión, que nos va a permitir comparar, de manera más gráfica y visual, la capacidad predicitva de
#nuestro modelo. Básicamente, obtendremos una cuadrícula 2x2 con los valores de la variable predicha (Yes 'predicho', No 'predicho'), y los valores de la variable
#real (Yes 'real', No 'real'). Esto nos permiten comparar cuántos valores predichos coinciden con los reales.
cm_disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels= reg_model.classes_) #Generamos la matriz de confusión, extrayendo las etiquetas con el modelo
cm_disp.plot(cmap=plt.cm.Blues) #Ploteamos la matriz de confusión con la paleta de colores de elección.
plt.show()

#Como se puede ver, este modelo nos da un buen valor de 'accuracy' (~0.85), pero un mal valor de 'precision' (~0.43), lo ccual podemos corroborar en nuestra matriz
#de confusión. Como se puede observar, la predicción de los valores 'No' es bastante buena, pero el modelo presenta problemas para predecir los 'Sí'; el modelo otorga
#un valor predicho de 'Sí' a un mayor número de valores reales 'No' que de reales 'Sí', por lo tanto tenemos un problema de falsos positivos con nueastro modelo.
#A partir de aquí, la primera opción que tenemos es modificar parámetros de nuestro modelo de regresión: cambiar el solver, modificar el número de interacciones,
#cambiar el valor de C, etc., o incluso modificar otras variables que aquí no he añadido, como la penalización ('penalty'). Sin embargo, para manipular estos parámetros
#de manera efectiva, considero que hacen falta conocimientos avanzados con respecto a estos modelos.

#Cabe decir que la regresión logística no es la única manera de desarrollar un modelo predictivio con nuestros datos, ya que disponemos de otros diferentes.
#Por ejemplo, el modelo de árbol de regresión que, considerando que ya tenemos los datos pre-tratados y la estructura del código escrita, no nos cuesta nada
#hacer una prueba con ese modelo. Este modelo se basa en un algoritmo en forma de árboles de decisión, de manera que cada nodo se correspone a un test, cada
#rama se corresponde al resultado de un test, y cada 'hoja' asigna su dato a una clase:
tree_clasi = DecisionTreeClassifier(max_depth=7, random_state=27) #max_depeth -> Profundidad máxima que queremos que alcancen las ramas (es decir, los desdobles),
#y nuevamente podemos configurar un random_state
tree_clasi.fit(encoded_data, y_train)
y_pred1 = tree_clasi.predict(encoded_data1)
print(f'The accuracy of the model is {accuracy_score(y_test, y_pred1)}')
print(f'The precision of the test is {precision_score(y_test, y_pred1)}')
print('--------------------')
cm1 = confusion_matrix(y_test, y_pred1)
cm_disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels= tree_clasi.classes_)
cm_disp1.plot(cmap=plt.cm.Blues)
plt.show()

#Como podemos observar, este modelo mejora notablemente la 'precision (~0.60), y ligeramente la 'accuracy' (~0.90). Nuevamente, con conocimientos avanzados sobre estos
#modelos se podrían manipular varios parámetros del modelo para ir ajustando la precisión del mismo.