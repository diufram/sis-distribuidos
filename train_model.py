import tensorflow as tf
import matplotlib.pyplot as ptl
import cv2
import numpy as np
#Aqui se importan las imagenes 
datos = []

TAMANO_IMG = 200

for i,(imagen,etiqueta) in enumerate(datos['train'].take(1)):
    imagen = cv2.resize(imagen.numpy(),(TAMANO_IMG,TAMANO_IMG))
    imagen =cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
    ptl.subplot(1,2,i+1)
    ptl.imshow(imagen,cmap='gray')

datos_entrenamiento = []

for i,(imagen,etiqueta) in enumerate(datos['train'].take(1)):
    imagen = cv2.resize(imagen.numpy(),(TAMANO_IMG,TAMANO_IMG))
    imagen =cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
    imagen = imagen.reshape(TAMANO_IMG,TAMANO_IMG,1) #Cambio de tamano a 100,100,1
    datos_entrenamiento.append([imagen,etiqueta])

datos_entrenamiento[0]

len(datos_entrenamiento) # Candidad de elementros del arreglo 

X = [] #imagenes de entrada (pixeles)
y = [] #etiquetas (perro o gato)

for imagen,etiqueta in datos_entrenamiento:
    X.append(imagen)
    y.append(etiqueta)

#Normalizando 
X = np.array(X).astype(float) / 255

y = np.array(y)

""" modeloDenso = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(100,100,1)),
    tf.keras.layers.Dense(150,activation='relu'),
    tf.keras.layers.Dense(150,activation='relu'),
    tf.keras.layers.Dense(1,activation='sigmoid'),
])
 """
modeloCNN = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32,(3,3),activation ='relu', input_shape=(100,100,1)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64,(3,3),activation ='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128,(3,3),activation ='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100,activation = 'relu'),
    tf.keras.layers.Dense(1,activation='sigmoid'),
])

""" modeloCNN2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32,(3,3),activation ='relu', input_shape=(100,100,1)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64,(3,3),activation ='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128,(3,3),activation ='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100,activation = 'relu'),
    tf.keras.layers.Dense(1,activation='sigmoid'),
])
 """
""" modeloDenso.compile(optimizer= 'adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
 """
modeloCNN.compile(optimizer= 'adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

""" modeloCNN2.compile(optimizer= 'adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
 """
#Importando el generador de aumento de datos 


datagen = tf.keras.preprocessing.img.ImageDataGenerator(
    rotation_range = 50, #Rotando las imagenes de manera aleatoria
    width_shift_range=0.2,
    height_shift_range = 0.2,
    shear_range= 15,
    zoom_range=[0.7,1.4],
    horizontal_flip=True,
    vertical_flip = True
)

datagen.fit(X)

X_entrenamiento =X[:1000]
X_validacion =X[:1000]

y_entrenamiento =y[:1000]
y_validacion =y[:1000]

data_gen_entrenamiento = datos.flow(X_entrenamiento,y_entrenamiento,batch_size= 32)

modeloCNN.fit(
    data_gen_entrenamiento,
    epochs=100,
    batch_size =32,
    validation_data=(X_validacion,y_validacion),
    steps_per_epoch=int(np.ceil(len(X_entrenamiento)/ float(32))),
    validation_steps=int(np.ceil(len(X_validacion)/ float(32))),
    )

modeloCNN.save('mdoel.h5')