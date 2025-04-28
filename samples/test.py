def add(a, b):
    return a + b


def multiply(x, y=2):
    return x * y


def relu(x):
    output = np.maximum(0, x)
    return output
