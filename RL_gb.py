import tensorflow as tf
import numpy as np
import scipy.special as sc


class ParallelMultilayerPerceptron:
    """A parallel multilayer perceptron network with fast predict calls."""

    def __init__(self, input_dim, hidden_layers):
        self.network = self._build_network(input_dim, hidden_layers)
        self.weights = self.get_weights()
        self.trainable_variables = self.network.trainable_variables

    def predict(self, X, **kwargs):
        for i, (m, b) in enumerate(self.weights):
            X = np.dot(X, m) + b
            print("before layer output", X.shape)
            if i == len(self.weights)-1:
                X = sc.log_softmax(X, axis=1).squeeze(axis=-1)
            else:
                X = np.maximum(X, 0, X)
            print("layer output", X.shape)
        return X

    def __call__(self, inputs):
        return self.network(inputs)[0]

    def get_logits(self, inputs):
        return self.network(inputs)[1]

    def save_weights(self, filename):
        self.network.save_weights(filename)

    def load_weights(self, filename):
        self.network.load_weights(filename)
        self.weights = self.get_weights()

    def get_weights(self):
        network_weights = self.network.get_weights()
        self.weights = []
        for i in range(len(network_weights)//2):
            m = network_weights[2*i].squeeze(axis=0)
            b = network_weights[2*i + 1]
            self.weights.append((m, b))
        return self.weights

    def _build_network(self, input_dim, hidden_layers):
        inputs = tf.keras.Input(shape=(None, input_dim))
        x = inputs
        for hidden in hidden_layers:
            x = tf.keras.layers.Conv1D(hidden, 1, activation='relu')(x)
        x = tf.keras.layers.Conv1D(1, 1, activation='linear')(x)
        outputs = tf.nn.log_softmax(x, axis=1)
        logprobs = tf.keras.layers.Flatten()(outputs)
        return tf.keras.Model(inputs=inputs, outputs=[logprobs, outputs])


def test_ParallelMultilayerPerceptron():
    policy = ParallelMultilayerPerceptron(3, [5])
    print(policy.weights)
    print(policy.network.get_weights())
    np.random.seed(123)
    X = np.random.randn(10, 7, 3)
    print("-------------------------------------")
    print("input ", X.shape)

    assert np.allclose(policy.predict(X), policy.network.predict(X)[0])

test_ParallelMultilayerPerceptron()