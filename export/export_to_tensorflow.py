import json
import os
from keras.engine.training import Model
import tensorflow as tf
from keras import backend as K
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import graph_io

dirname = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(dirname, '..', 'data', 'model', 'model_best_config.json')
weight_file_path = os.path.join(dirname, '..', 'data', 'model', 'model_best_weight.h5')

model = None
with open(config_file_path, "rt") as f:
    model = Model.from_config(json.load(f))
model.load_weights(weight_file_path)

K.set_learning_phase(0)
K.set_image_data_format('channels_last')

num_output = 1
pred = [None]*num_output
pred_node_names = [None]*num_output
for i in range(num_output):
    pred_node_names[i] = 'output_node' + str(i)
    pred[i] = tf.identity(model.outputs[i], name=pred_node_names[i])

sess = K.get_session()

constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(), pred_node_names)
graph_io.write_graph(constant_graph, dirname, 'model.pb', as_text=False)

