# -*- coding: utf-8 -*-
"""estrellas.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Mc2W6vwoeUrUjv9X-PxLhESkKJM8Ab9w
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


df = pd.read_csv("Laboratorio_A00834760/Portafolio2/star_data.csv")
df.head()

df = df[['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)', 'Star type', 'Star color', 'Spectral Class']]
df.head()

# Replace blank spaces with NaN
df['Star color'] = df['Star color'].replace(' ', np.nan)
# Impute missing values with the mode (most frequent value)
most_common_color = df['Star color'].mode()[0]
df['Star color'].fillna(most_common_color, inplace=True)

print(df['Star color'].unique())

df['Temperature (K)'] = pd.to_numeric(df['Temperature (K)'], errors='coerce')
df['Luminosity(L/Lo)'] = pd.to_numeric(df['Luminosity(L/Lo)'], errors='coerce')
df['Radius(R/Ro)'] = pd.to_numeric(df['Radius(R/Ro)'], errors='coerce')
df['Absolute magnitude(Mv)'] = pd.to_numeric(df['Absolute magnitude(Mv)'], errors='coerce')
df.head()

df.dropna(inplace=True)
df.head()

df_nums = df[['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)', 'Star type']]

sns.heatmap(df_nums.corr(), annot=True)
plt.title('Heatmap of numeric feautures')
plt.show()

"""## Portafolio 1
En esta seccion esta la implementacion de uno de los algoritmos vistos en el módulo sin uso de ninguna biblioteca o framework de aprendizaje máquina, ni de estadística avanzada. Lo que se busca es que se implemente manualmente el algoritmo.
"""

import math

def sigmoid_function(X):
  return 1/(1+math.e**(-X))

def log_regression4(X, y, alpha, epochs):
  y_ = np.reshape(y, (len(y), 1)) # shape (150,1)
  N = len(X)
  theta = np.random.randn(len(X[0]) + 1, 1) #* initialize theta
  X_vect = np.c_[np.ones((len(X), 1)), X] #* Add x0 (column of 1s)
  avg_loss_list = []
  loss_last_epoch = 9999999
  for epoch in range(epochs):
    sigmoid_x_theta = sigmoid_function(X_vect.dot(theta)) # shape: (150,5).(5,1) = (150,1)
    grad = (1/N) * X_vect.T.dot(sigmoid_x_theta - y_) # shapes: (5,150).(150,1) = (5, 1)
    best_params = theta
    theta = theta - (alpha * grad)
    hyp = sigmoid_function(X_vect.dot(theta)) # shape (150,5).(5,1) = (150,1)
    avg_loss = -np.sum(np.dot(y_.T, np.log(hyp) + np.dot((1-y_).T, np.log(1-hyp)))) / len(hyp)
    # if epoch % 50 == 0:
    #   print('epoch: {} | avg_loss: {}'.format(epoch, avg_loss))
    #   print('')
    avg_loss_list.append(avg_loss)
    loss_step = abs(loss_last_epoch - avg_loss) #*
    loss_last_epoch = avg_loss #*
    # if loss_step < 0.001: #*
    #   # print('\nStopping training on epoch {}/{}, as (last epoch loss - current epoch loss) is less than 0.001 [{}]'.format(epoch, epochs, loss_step)) #*
    #   break #*
  # plt.plot(np.arange(1, epoch+1), avg_loss_list[1:], color='red')
  # plt.title('Cost function')
  # plt.xlabel('Epochs')
  # plt.ylabel('Cost')
  # plt.show()
  return best_params

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load Dataset
# iris = datasets.load_iris()
# Define X features
data = df[['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']].to_numpy()
target = df['Star type'].to_numpy()
# print(iris['Star type'])
# Define binary Star type 'y' based on iris plant type
#0-Brown Dwarf, 1-Red Dwarf, 2-White Dwarf, 3-Main Sequence, 4-Supergiants, 5-Hypergiants
y_Brown_Dwarf = (target == 0).astype(int)
y_Red_Dwarf = (target == 1).astype(int)
y_White_Dwarf = (target == 2).astype(int)
y_Main_Sequence = (target == 3).astype(int)
y_Supergiants = (target == 4).astype(int)
y_Hypergiants = (target == 5).astype(int)
# List of ys
y_iris_types = [y_Brown_Dwarf, y_Red_Dwarf, y_White_Dwarf, y_Main_Sequence, y_Supergiants, y_Hypergiants]
y_iris_types = {
    'Brown Dwarf': y_Brown_Dwarf,
    'Red Dwarf': y_Red_Dwarf,
    'White Dwarf': y_White_Dwarf,
    'Main Sequence': y_Main_Sequence,
    'Supergiants': y_Supergiants,
    'Hypergiants': y_Hypergiants
}
predicted_probs = {
    'Brown Dwarf': 0,
    'Red Dwarf': 0,
    'White Dwarf': 0,
    'Main Sequence': 0,
    'Supergiants': 0,
    'Hypergiants': 0
}
actual_y = {
    'Brown Dwarf': 0,
    'Red Dwarf': 0,
    'White Dwarf': 0,
    'Main Sequence': 0,
    'Supergiants': 0,
    'Hypergiants': 0
}
for key, y_iris_type in y_iris_types.items():
  # Split dataset (training and testing sets)
  X_train, X_test, y_train, y_test = train_test_split(data, y_iris_type, test_size=0.2, random_state=0)
  # Scale X
  sc = StandardScaler()
  X_train = sc.fit_transform(X_train)
  X_test = sc.transform(X_test)
  # Train model
  epochs = 1000
  alpha = 1
  best_params = log_regression4(X_train, y_train, alpha, epochs)
  # Make predictions on test set
  index_ = 5
  X_to_predict = [list(X_test[index_])]
  # print(X_to_predict)
  X_to_predict = np.c_[np.ones((len(X_to_predict), 1)), X_to_predict] # add x0 for bias
  # print(X_to_predict)
  pred_probability = sigmoid_function(X_to_predict.dot(best_params))
  predicted_probs[key] = pred_probability[0][0]
  print('Our model calculated probability of sample being {}, is: {}%'.format(key, round(pred_probability[0][0]*100,2)))
  actual_y[key] = y_test[index_]

max_key = max(predicted_probs, key=predicted_probs.get)
print('\n', predicted_probs)
print('\nModel Prediction: {}'.format(max_key))
max_actual_y = max(actual_y, key=actual_y.get)
print('Real value is: {}'.format(max_actual_y))

"""## Portafolio 2

En esta seccion encontramos el algoritmo de Random Forest haciendo uso de una biblioteca y framework de aprendizaje máquina. Lo que se busco fue demostrar el conocimiento sobre el framework y como configurar el algoritmo.
Se ha probado la implementación con el set de datos de Estrellas y se han realizado algunas predicciones.

"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, confusion_matrix, classification_report

x = df[['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']]
y = df['Star type']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

random_forest = RandomForestClassifier().fit(x_train, y_train)
y_pred = random_forest.predict(x_test)

random_forest = RandomForestClassifier(
    n_estimators=100,
    max_depth=2,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='log2',
    random_state=21
)

# Ajustar el modelo a los datos de entrenamiento
random_forest.fit(x_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = random_forest.predict(x_test)

# Métricas
print('Score de exactitud:', accuracy_score(y_test, y_pred))
print('Score de precisión:', precision_score(y_test, y_pred, average='weighted'))
print('Score f1:', f1_score(y_test, y_pred, average='weighted'))
print('Score de recall:', recall_score(y_test, y_pred, average='weighted'))

# Matriz de confusión
mat = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{mat}')

# Reporte de clasificación
reporte = classification_report(y_test, y_pred)
print(f'Classification Report:\n{reporte}')