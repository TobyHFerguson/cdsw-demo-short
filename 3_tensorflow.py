import tensorflow as tf
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import utils

### Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('data/MNIST/', one_hot=True)

### View Data
for i in xrange(0, 3):
  tmp = mnist.train.images[i]
  tmp = tmp.reshape((28,28))
  plt.imshow(tmp, cmap = cm.Greys)
  plt.show()

### Parameters
learning_rate = 0.01
training_epochs = 5
batch_size = 100
display_step = 1
logs_path = '/tmp/tensorboard'

### Cleanup old logs
if tf.gfile.Exists(logs_path):
  tf.gfile.DeleteRecursively(logs_path)
tf.gfile.MakeDirs(logs_path)

### Model
# Use a single-layer perceptron as example $pred = softmax(W x+b)$.
x = tf.placeholder('float', [None, 784], name='data')
y = tf.placeholder('float', [None, 10], name='label')

# Model bias and weight variables: W, b
W = tf.Variable(tf.zeros([784,10]), name='weights')
b = tf.Variable(tf.zeros([10]), name='bias')

# Put the model ops into scopes for tensorboard
with tf.name_scope('Model'):
    logits = tf.matmul(x,W)+b
    pred = tf.nn.softmax( logits )
with tf.name_scope('Loss'):
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))
with tf.name_scope('sgd'):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
with tf.name_scope('evaluation'):
    corr_pred = tf.equal( tf.argmax(pred,1), tf.argmax(y,1) )
    acc = tf.reduce_mean(tf.cast(corr_pred, 'float'))

init = tf.global_variables_initializer()

### Summaries
# Create *summary* ops to monitor the cost/accuracy

loss_summary = tf.summary.scalar('loss', cost)
accu_summary = tf.summary.scalar('accuracy', acc)

merged_summary_op = tf.summary.merge([loss_summary, accu_summary])

## Fit Model
sess = tf.Session()
sess.run(init)

# Write tensboard summaries
summary_writer = tf.summary.FileWriter(logdir=logs_path, graph=tf.get_default_graph())

for epoch in xrange(1, training_epochs+1):
    avg_cost = 0
    total_batch = int(mnist.train.num_examples/batch_size)
    for i in xrange(total_batch):
        xs, ys = mnist.train.next_batch(batch_size)
        _, c, summary = sess.run([optimizer, cost, merged_summary_op],
                                feed_dict = {x:xs, y:ys})
        summary_writer.add_summary(summary, epoch*total_batch+i)
        avg_cost += c/total_batch
    if epoch % display_step == 0:
        print('epoch %4d, cost = %.9f' % (epoch, avg_cost))
print("Accuracy: %f" % acc.eval(session=sess, feed_dict={x: mnist.test.images, y: mnist.test.labels}))
summary_writer.close()

### Examine layers    
# A red/black/blue colormap
cdict = {'red':   [(0.0,  1.0, 1.0),
                    (0.25,  1.0, 1.0),
                    (0.5,  0.0, 0.0),
                    (1.0,  0.0, 0.0)],
        'green': [(0.0,  0.0, 0.0),
                    (1.0,  0.0, 0.0)],
        'blue':  [(0.0,  0.0, 0.0),
                       (0.5,  0.0, 0.0),
                       (0.75, 1.0, 1.0),
                       (1.0,  1.0, 1.0)]}
redblue = matplotlib.colors.LinearSegmentedColormap('red_black_blue',cdict,256)

wts = W.eval(sess)
for i in range(0,5):
    im = wts.flatten()[i::10].reshape((28,-1))
    plt.imshow(im, cmap = redblue, clim=(-1.0, 1.0))
    plt.colorbar()
    print("Digit %d" % i)
    plt.show()

### Explore using Tensorboard
utils.start_tensorboard(logs_path, iframe=False)