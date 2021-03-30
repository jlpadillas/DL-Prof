#!/usr/bin/env python
# coding: utf-8

# Primera prueba:
# 
# vamos a aislar en un core a tensorflow, y vamos a medir con perf los eventos de dicho core.
# 
# vamos a hacer una ejecución corta de mnist.py, una sola época (puedes usar el código que ya tienes, mira a ver cómo se define el número de epochs), un solo thread (bajar intra e inter op parallelism a 1) y medir con perf.
# 
# Las stats que yo sacaría son: instrucciones totales, ciclos totales, instrucciones de punto flotante (ojo con estas, te va a tocar buscar cuales son de todas las disponibles en los eventos!!).
# 
# Comando: perf -e XXXX -C <n> taskset -c <n>x mnist_1epoch_1thread.py

# -----

# Python ≥3.5 is required
import sys
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"

try:
    # %tensorflow_version only exists in Colab.
    get_ipython().run_line_magic('tensorflow_version', '2.x')
except Exception:
    pass

# TensorFlow ≥2.0 is required
import tensorflow as tf
assert tf.__version__ >= "2.0"

# Common imports
import numpy as np
import os

# to make this notebook's output stable across runs
np.random.seed(42)

# To plot pretty figures
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "ann"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)
os.makedirs(IMAGES_PATH, exist_ok=True)

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


from tensorflow import keras

print("tf version " + tf.__version__)
print("keras version " + keras.__version__)


# Obtengo el numero de threads por defecto:
tf.config.threading.get_inter_op_parallelism_threads()
tf.config.threading.get_intra_op_parallelism_threads()

# Configuro el intra y el inter a 1:
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)

tf.config.threading.get_inter_op_parallelism_threads()
tf.config.threading.get_intra_op_parallelism_threads()


# Empieza la ejecucion de MNIST
fashion_mnist = keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

X_train_full.shape
X_train_full.dtype

X_valid, X_train = X_train_full[:5000] / 255., X_train_full[5000:] / 255.
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.

plt.imshow(X_train[0], cmap="binary")
plt.axis('off')
plt.show()

y_train


class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]



class_names[y_train[0]]


X_valid.shape

X_test.shape


n_rows = 4
n_cols = 10
plt.figure(figsize=(n_cols * 1.2, n_rows * 1.2))
for row in range(n_rows):
    for col in range(n_cols):
        index = n_cols * row + col
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(X_train[index], cmap="binary", interpolation="nearest")
        plt.axis('off')
        plt.title(class_names[y_train[index]], fontsize=12)
plt.subplots_adjust(wspace=0.2, hspace=0.5)
save_fig('fashion_mnist_plot', tight_layout=False)
plt.show()

model = keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=[28, 28]))
model.add(keras.layers.Dense(300, activation="relu"))
model.add(keras.layers.Dense(100, activation="relu"))
model.add(keras.layers.Dense(10, activation="softmax"))

model.layers



model.summary()


keras.utils.plot_model(model, "my_fashion_mnist_model.png", show_shapes=True)


hidden1 = model.layers[1]
hidden1.name

model.get_layer(hidden1.name) is hidden1


weights, biases = hidden1.get_weights()


weights



weights.shape



biases


biases.shape


# In[33]:


model.compile(loss="sparse_categorical_crossentropy",
              optimizer="sgd",
              metrics=["accuracy"])


# Para ver los dispositivos que puedo usar:

# In[34]:


tf.config.list_physical_devices(
    device_type=None
)


# In[35]:


tf.config.list_logical_devices(
    device_type=None
)


# In[36]:


tf.config.get_visible_devices(
    device_type=None
)


# In[37]:


tf.config.experimental.get_device_policy()


# In[38]:


physical_devices = tf.config.list_physical_devices('CPU')
assert len(physical_devices) == 1, "No CPUs found"
configs = tf.config.get_logical_device_configuration(
  physical_devices[0])
try:
  assert configs is None
  tf.config.set_logical_device_configuration(
    physical_devices[0],
    [tf.config.LogicalDeviceConfiguration(),
     tf.config.LogicalDeviceConfiguration()])
  configs = tf.config.get_logical_device_configuration(
    physical_devices[0])
  assert len(configs) == 2
except:
  # Cannot modify virtual devices once initialized.
  pass


# In[39]:


tf.config.get_visible_devices(
    device_type=None
)


# In[40]:


tf.config.experimental.get_device_policy()


# In[41]:


tf.device(
    '/device:XLA_CPU:0'
)


# In[ ]:





# In[ ]:





# In[ ]:





# In[42]:


history = model.fit(X_train, y_train, epochs=1,
                    validation_data=(X_valid, y_valid))


# In[ ]:


history.params


# In[ ]:


print(history.epoch)


# In[ ]:


history.history.keys()


# In[ ]:




