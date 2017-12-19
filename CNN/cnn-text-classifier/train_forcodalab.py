#! /usr/bin/env python
# 2017-12-01 : added options to load pretrained word2vec embedding
#              added decay_coefficient
import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers
import math
from text_cnn import TextCNN
from tensorflow.contrib import learn

# Parameters
# ==================================================

# Data loading params
tf.flags.DEFINE_float("dev_sample_percentage", .1, "Percentage of the training data to use for validation")
tf.flags.DEFINE_string("positive_data_file", "./data/rt-polaritydata/rt-polarity.pos", "Data source for the positive data.")
tf.flags.DEFINE_string("negative_data_file", "./data/rt-polaritydata/rt-polarity.neg", "Data source for the negative data.")
tf.flags.DEFINE_string("configuration_file","./cfg.yml","Data source for embedding layer configuration file.")


# Model Hyperparameters
tf.flags.DEFINE_boolean("enable_word_embeddings",True,"Enable/disable pretrained word embedding (default: True)")
tf.flags.DEFINE_integer("embedding_dim", 128, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "3,4", "Comma-separated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")

# Training parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (default: 100)")
tf.flags.DEFINE_integer("num_checkpoints", 5, "Number of checkpoints to store (default: 5)")
tf.flags.DEFINE_float("random_seed",10.0,"seed for randomly shuffling the data (default: 10.0)")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
tf.flags.DEFINE_float("decay_coefficient",2.5,"Decay coefficient (default: 2.5)")

FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")

# Embedding Preparation
# =================================================
# with open(FLAGS.configuration_file,'r') as ymlfile:
#     cfg = yaml.load(ymlfile)
if FLAGS.enable_word_embeddings:
    embedding_name  = 'word2vec'
    embedding_dimension = 64
else:
    embedding_dimension = FLAGS.embedding_dim



# Data Preparation
# ==================================================

# Load data
print("Loading data...")
x_text, y = data_helpers.load_data_and_labels(FLAGS.positive_data_file, FLAGS.negative_data_file)

# Build vocabulary
max_document_length = max([len(x.split(" ")) for x in x_text])
vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length//2)
x = np.array(list(vocab_processor.fit_transform(x_text)))

# Randomly shuffle data
np.random.seed(10)
shuffle_indices = np.random.permutation(np.arange(len(y)))
x_shuffled = x[shuffle_indices]
y_shuffled = y[shuffle_indices]

# Split train/test set
# TODO: This is very crude, should use cross-validation
dev_sample_index = -1 * int(FLAGS.dev_sample_percentage * float(len(y)))
x_train, x_dev = x_shuffled[:dev_sample_index], x_shuffled[dev_sample_index:]
y_train, y_dev = y_shuffled[:dev_sample_index], y_shuffled[dev_sample_index:]
print("Vocabulary Size: {:d}".format(len(vocab_processor.vocabulary_)))
print("Train/Dev split: {:d}/{:d}".format(len(y_train), len(y_dev)))


# Training
# ==================================================

with tf.Graph().as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=FLAGS.allow_soft_placement,
      log_device_placement=FLAGS.log_device_placement)
    session_conf.gpu_options.allow_growth = True ##allow memory grow for GPU
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        cnn = TextCNN(
            sequence_length=x_train.shape[1],
            num_classes=y_train.shape[1],
            vocab_size=len(vocab_processor.vocabulary_),
            embedding_size=embedding_dimension, ## modified here !
            filter_sizes=list(map(int, FLAGS.filter_sizes.split(","))),
            num_filters=FLAGS.num_filters,
            l2_reg_lambda=FLAGS.l2_reg_lambda)

        # Define Training procedure
        global_step = tf.Variable(0, name="global_step", trainable=False)
        optimizer = tf.train.AdamOptimizer(1e-3)
        grads_and_vars = optimizer.compute_gradients(cnn.loss)
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

        # Keep track of gradient values and sparsity (optional)
        #print (grads_and_vars)
        grad_summaries = []
        for g, v in grads_and_vars:
            if g is not None:
                print("Gradient is not None!")
                grad_hist_summary = tf.summary.histogram("{}/grad/hist".format(v.name), g)
                sparsity_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
                grad_summaries.append(grad_hist_summary)
                grad_summaries.append(sparsity_summary)
            else:
                print ("Gradient is None!")
        grad_summaries_merged = tf.summary.merge(grad_summaries)

        # Output directory for models and summaries
        timestamp = str(int(time.time()))
        out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
        print("Writing to {}\n".format(out_dir))

        # Summaries for loss and accuracy
        loss_summary = tf.summary.scalar("loss", cnn.loss)
        acc_summary = tf.summary.scalar("accuracy", cnn.accuracy)

        # Train Summaries
        train_summary_op = tf.summary.merge([loss_summary, acc_summary, grad_summaries_merged])
        train_summary_dir = os.path.join(out_dir, "summaries", "train")
        train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

        # Dev summaries
        dev_summary_op = tf.summary.merge([loss_summary, acc_summary])
        dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
        dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)

        # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
        checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
        checkpoint_prefix = os.path.join(checkpoint_dir, "model")
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=FLAGS.num_checkpoints)

        # Write vocabulary
        vocab_processor.save(os.path.join(out_dir, "vocab"))

        # Initialize all variables
        sess.run(tf.group(tf.global_variables_initializer(), tf.local_variables_initializer()))
        if FLAGS.enable_word_embeddings:
            # load embedding vectors from the word2vec
            print("Load word2vec file {}".format('./yelp_word2vec.bin'))
            vocabulary = vocab_processor.vocabulary_
            initW = data_helpers.load_embedding_vectors_word2vec(vocabulary,'./yelp_word2vec.bin',True)
            print("word2vec file has been loaded")

            sess.run(cnn.W.assign(initW))
        # # test print W
        # a = sess.run(cnn.embedded_chars)
        # a = tf.Print(a, [a], message="This is embedded chars: ")
        # b = tf.add(a, a).eval()
        # print (b.shape)
        #
        # c = sess.run(cnn.embedded_chars_expanded)
        # d = tf.Print(c, [c], message="This is embedded chars expanded: ")
        # d = tf.add(c, c).eval()
        # print (d.shape)

        # np.save("./W_got.npy", W_got)

        def train_step(x_batch, y_batch,learning_rate): ## added learning_rate here
            """
            A single training step
            """
            feed_dict = {
              cnn.input_x: x_batch,
              cnn.input_y: y_batch,
              cnn.dropout_keep_prob: FLAGS.dropout_keep_prob,
              cnn.learning_rate: learning_rate
            }
            _, step, summaries, loss, accuracy,precision,recall = sess.run(
                [train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy,cnn.precision,cnn.recall],
                feed_dict)

            time_str = datetime.datetime.now().isoformat()
            print("{}: step {}, loss {:g}, acc {:g},prec {:g},recall {:g},learning_rate {:g}".format(time_str, step, loss, accuracy,precision,recall,learning_rate))
            train_summary_writer.add_summary(summaries, step)

        def dev_step(x_batch, y_batch, writer=None):
            """
            Evaluates model on a dev set
            """
            batches = data_helpers.batch_iter(
                list(zip(x_batch, y_batch)), FLAGS.batch_size, 1,False)
            final_loss=0
            final_accuracy=0
            final_precision=0
            final_recall=0
            count=0
            for batch in batches:
                count+=1
                x_tmp, y_tmp = zip(*batch)
                feed_dict = {
                  cnn.input_x: x_tmp,
                  cnn.input_y: y_tmp,
                  cnn.dropout_keep_prob: 1.0
                }
                step, summaries, loss, accuracy,precision,recall = sess.run(
                    [global_step, dev_summary_op, cnn.loss, cnn.accuracy,cnn.precision, cnn.recall],
                    feed_dict)
                time_str = datetime.datetime.now().isoformat()
                print("{}: step {}, loss {:g}, acc {:g},precision {:g},recall {:g}".format(time_str, step, loss, accuracy,precision,recall))
                if writer:
                    writer.add_summary(summaries, step)
                final_loss+=loss
                final_accuracy+=accuracy
                final_precision += precision
                final_recall += recall
            final_loss = float(final_loss)/count
            final_recall = float(final_recall)/count
            final_accuracy = float(final_accuracy)/count
            final_precision = float(final_precision)/count
            print("final eval {}: step {}, loss {:g}, acc {:g},precision {:g},recall {:g}".format(time_str, step, final_loss, final_accuracy,final_precision,final_recall))


        # Generate batches
        batches = data_helpers.batch_iter(
            list(zip(x_train, y_train)), FLAGS.batch_size, FLAGS.num_epochs)

        # It uses dynamic learning rate with  a high value at the beginning to speed up the trarining
        max_learning_rate = 0.005
        min_learning_rate = 0.0001
        decay_speed = FLAGS.decay_coefficient * len(y_train)/FLAGS.batch_size

        # Training loop. For each batch...
        counter = 0
        for batch in batches:
            learning_rate = min_learning_rate + (max_learning_rate - min_learning_rate) * math.exp(-counter/decay_speed)
            counter += 1
            x_batch, y_batch = zip(*batch)
            train_step(x_batch, y_batch,learning_rate)
            current_step = tf.train.global_step(sess, global_step)
            if current_step % FLAGS.evaluate_every == 0:
                print("\nEvaluation:")
                dev_step(x_dev, y_dev, writer=dev_summary_writer)
                print("")
            if current_step % FLAGS.checkpoint_every == 0:
                path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                print("Saved model checkpoint to {}\n".format(path))
