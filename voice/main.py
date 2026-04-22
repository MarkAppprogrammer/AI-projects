import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
import data
import math

#custom layers
class SubSpectralNorm(tf.keras.layers.Layer):
    def __init__(self, subbands=5, eps=1e-5):
        super().__init__()
        self.subbands = subbands
        self.eps = eps

    def call(self, x):
        b, c, f, w = tf.shape(x)[0], tf.shape(x)[1], tf.shape(x)[2], tf.shape(x)[3]
        g = self.subbands
        f_per_g = f // g
        x = tf.reshape(x, (b, c, g, f_per_g, w))
        mean, var = tf.nn.moments(x, axes=[3], keepdims=True)
        x = (x - mean) / tf.sqrt(var + self.eps)
        return tf.reshape(x, (b, c, f, w))

class BC_ResNetBlock(tf.keras.Model):
    def __init__(self, channels, stride, dilation, p=0.1, transition=False, blocknum=0):
        super(BC_ResNetBlock, self).__init__(name=f"bc_resnet_block_{blocknum}")
        self.transition = transition

        if (transition):
            self.pointwise1 = tf.keras.layers.Conv2D(
                kernel_size=(1,1),
                filters=channels,
                padding="same",
                data_format="channels_first"
            )
            self.bn1 = tf.keras.layers.BatchNormalization(axis=1)
            self.relu = tf.keras.layers.Activation('relu')

        self.dwconv1 = tf.keras.layers.DepthwiseConv2D(
            kernel_size=(3, 1),
            padding="same", # was same
            strides=stride,
            data_format="channels_first"
        )
        self.ssn = SubSpectralNorm()

        self.dwconv2 = tf.keras.layers.DepthwiseConv2D(
            kernel_size=(1, 5),   # temporal kernel
            padding="same", # was same
            # strides=stride,
            data_format="channels_first",
            dilation_rate=dilation
        )
        self.bn2 = tf.keras.layers.BatchNormalization(axis=1)
        self.swish = tf.keras.layers.Activation('swish')
        self.pointwise2 = tf.keras.layers.Conv2D(
            kernel_size=(1,1),
            filters=channels,
            padding="same",
            data_format="channels_first"
        )
        
        self.dropout = tf.keras.layers.SpatialDropout2D(rate=p, data_format="channels_first")

    def call(self, input_tensor, training=False):
        b, c, h, w = input_tensor.shape
        x = input_tensor # for shortcut
        
        shortcut = x

        #pointwise + bn, relu for transition
        if self.transition:
            x = self.pointwise1(x)
            x = self.bn1(x)
            x = self.relu(x)

        #freq-dwconv + ssn (f2)
        x = self.dwconv1(x)
        x = self.ssn(x)

        x_res = x

        x = tf.reduce_mean(x, axis=2, keepdims=True) # freq avreage pool

        #temporal-dwconv + bn,swish + 1x1 conv dropout (f1)
        x = self.dwconv2(x)
        x = self.bn2(x)
        x = self.swish(x)
        x = self.pointwise2(x)
        x = self.dropout(x)

        #brodcasting
        # x = tf.repeat(x, repeats=h, axis=2)
        freq = x_res.shape[2]
        x = tf.repeat(x, repeats=freq, axis=2)

        #only use transition if in/out channels differ
        if self.transition:
            x = x_res + x
        else:
            x = shortcut + x_res + x
        
        return x

#model arch
model = Sequential([
    # tf.keras.Input(
    #     shape=(1, 40, 235), #channel x freq x time
    #     batch_size=32
    # ),
    tf.keras.layers.Input(shape=(1, 40, 98), batch_size=100),
    tf.keras.layers.Conv2D(
        filters=16,
        kernel_size=(5,5),
        strides=(2,1),
        dilation_rate=1,
        activation='relu',
        data_format="channels_first",
        padding="same"
    ),
    BC_ResNetBlock(channels=8, stride=1, dilation=1, transition=True, blocknum=1),
    BC_ResNetBlock(channels=8, stride=1, dilation=1, transition=False, blocknum=2),

    BC_ResNetBlock(channels=12, stride=(2,1), dilation=(1,2), transition=True, blocknum=3),
    BC_ResNetBlock(channels=12, stride=1, dilation=(1,2), transition=False, blocknum=4),

    BC_ResNetBlock(channels=16, stride=(2,1), dilation=(1,4), transition=True, blocknum=5),
    BC_ResNetBlock(channels=16, stride=1, dilation=(1,4), transition=False, blocknum=6),
    BC_ResNetBlock(channels=16, stride=1, dilation=(1,4), transition=False, blocknum=7),
    BC_ResNetBlock(channels=16, stride=1, dilation=(1,4), transition=False, blocknum=8),

    BC_ResNetBlock(channels=20, stride=1, dilation=(1,8), transition=True, blocknum=9),
    BC_ResNetBlock(channels=20, stride=1, dilation=(1,8), transition=False, blocknum=10),
    BC_ResNetBlock(channels=20, stride=1, dilation=(1,8), transition=False, blocknum=11),
    BC_ResNetBlock(channels=20, stride=1, dilation=(1,8), transition=False, blocknum=12),
    tf.keras.layers.DepthwiseConv2D(
        kernel_size=(5, 1),
        padding="same", 
        data_format="channels_first"
    ),
    tf.keras.layers.Conv2D( #pointwise
        kernel_size=(1,1),
        filters=32,
        padding="same",
        data_format="channels_first"
    ),
    tf.keras.layers.Lambda(
        lambda x: tf.reduce_mean(x, axis=[2,3], keepdims=True),
        name='avg_pool'
    ),
    tf.keras.layers.Conv2D(
        filters=12,
        kernel_size=(1,1),
        padding="same",
        data_format="channels_first"
    ),
    tf.keras.layers.Reshape((12,))
])

model.summary()
# print(data.test_files[0])

epochs = 200
batch_size = 100
warmup_epochs = 5
base_lr = 0.1
momentum = 0.9
weight_decay = 1e-3

steps_per_epoch = tf.data.experimental.cardinality(data.train_ds).numpy()
total_steps = epochs * steps_per_epoch
warmup_steps = warmup_epochs * steps_per_epoch
decay_steps = total_steps - warmup_steps


class WarmupCosineDecay(tf.keras.optimizers.schedules.LearningRateSchedule):
    def __init__(self, base_lr, warmup_steps, decay_steps):
        super().__init__()
        self.base_lr = base_lr
        self.warmup_steps = warmup_steps
        self.decay_steps = decay_steps

    def __call__(self, step):
        step = tf.cast(step, tf.float32)
        warmup_steps = tf.cast(self.warmup_steps, tf.float32)
        decay_steps = tf.cast(self.decay_steps, tf.float32)

        warmup_lr = self.base_lr * (step / tf.maximum(1.0, warmup_steps))
        cosine_step = tf.minimum(step - warmup_steps, decay_steps)
        cosine_decay = 0.5 * (1.0 + tf.cos(math.pi * cosine_step / tf.maximum(1.0, decay_steps)))
        decay_lr = self.base_lr * cosine_decay

        return tf.where(step < warmup_steps, warmup_lr, decay_lr)
    
lr_schedule = WarmupCosineDecay(base_lr, warmup_steps, decay_steps)

optimizer = tf.keras.optimizers.SGD(
    learning_rate=lr_schedule,
    momentum=momentum,
    nesterov=False
)

model.compile(
    optimizer=optimizer,
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    data.train_ds,
    validation_data=data.val_ds,
    epochs=epochs
)
# model.fit(
#     data.train_ds,
#     validation_data=data.val_ds,
#     epochs=200,
# )
