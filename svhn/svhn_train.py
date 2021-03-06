from __future__ import division
from __future__ import print_function

from datetime import datetime
import os.path
import time

import numpy as np
import tensorflow as tf
import svhn

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('train_dir', '/Users/ccuulinay/PycharmProjects/ml_course_test/deep_learning_udacity/svhn/tmp/mat/svhn_train',
                           """Directory where to write event logs """
                           """and checkpoint.""")
tf.app.flags.DEFINE_integer('max_steps', 50000,
                            """Number of batches to run.""")
# tf.app.flags.DEFINE_integer('max_steps', 1000000,
#                            """Number of batches to run.""")

tf.app.flags.DEFINE_boolean('log_device_placement', False,
                            """Whether to log device placement.""")

def train():
    """Train SVHN for a number of steps."""
    with tf.Graph().as_default():
        global_step = tf.Variable(0, trainable=False)
        # Get images and labels for SVHN with mat file
        images, labels = svhn.distorted_inputs()
        # Build a Graph that computes the logits predictions from
        # inference model.
        logits = svhn.inference(images)

        # Calculate loss.
        loss = svhn.loss(logits, labels)

        # Build a Graph that trains the model with one batch of examples
        # and updates the model parm
        train_op = svhn.train(loss, global_step)

        # Create a saver.
        saver = tf.train.Saver(tf.all_variables())

        # Build an initialization operation to run.
        init = tf.initialize_all_variables()

        # Start running operations on the Graph.
        sess = tf.Session(config=tf.ConfigProto(log_device_placement=FLAGS.log_device_placement))
        sess.run(init)

        # Start the queue runners.
        tf.train.start_queue_runners(sess=sess)

        # summary_writer = tf.train.SummaryWriter(FLAGS.train_dir, sess.graph)

        for step in xrange(FLAGS.max_steps):
            start_time = time.time()
            _, loss_value = sess.run([train_op, loss])
            duration = time.time() - start_time

            assert not np.isnan(loss_value), 'Model diverged with loss = NaN'

            if step % 10 == 0:
                num_examples_per_step = FLAGS.batch_size
                examples_per_sec = num_examples_per_step / duration
                sec_per_batch = float(duration)
                format_str = ('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f '
                              'sec/batch)')
                print (format_str % (datetime.now(), step, loss_value,
                                     examples_per_sec, sec_per_batch))

            # Save the model checkpoint periodically.
            if step % 1000 == 0 or (step +1) == FLAGS.max_steps:
                checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=step)


def main(argv=None):
    # svhn.maybe_download_and_extract()
    if tf.gfile.Exists(FLAGS.train_dir):
        tf.gfile.DeleteRecursively(FLAGS.train_dir)
    tf.gfile.MakeDirs(FLAGS.train_dir)
    train()


if __name__ == '__main__':
    tf.app.run()