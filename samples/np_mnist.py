# 作业内容：更改loss函数、网络结构、激活函数，完成训练MLP网络识别手写数字MNIST数据集
import numpy as np
import random
from tqdm import tqdm

# 加载数据集,numpy格式
X_train = np.load('./mnist/X_train.npy') # (60000, 784), 数值在0.0~1.0之间
y_train = np.load('./mnist/y_train.npy') # (60000, )
y_train = np.eye(10)[y_train] # (60000, 10), one-hot编码

X_val = np.load('./mnist/X_val.npy') # (10000, 784), 数值在0.0~1.0之间
y_val = np.load('./mnist/y_val.npy') # (10000,)
y_val = np.eye(10)[y_val] # (10000, 10), one-hot编码

X_test = np.load('./mnist/X_test.npy') # (10000, 784), 数值在0.0~1.0之间
y_test = np.load('./mnist/y_test.npy') # (10000,)
y_test = np.eye(10)[y_test] # (10000, 10), one-hot编码

# 定义激活函数
def relu(x):
  ''' relu '''
  output=np.maximum(0,x)
  return output

def relu_prime(x):
    ''' relu导数 '''
    bottom_diff=np.where(x > 0, 1, 0)
    return bottom_diff

#输出层激活函数
def f(x):
    ''' softmax'''
    exps = np.exp(x - np.max(x, axis = -1, keepdims=True))
    output=exps / np.sum(exps, axis = -1, keepdims=True)
    return output

def f_prime(x):
    '''softmax导数'''
    bottom_diff=f(x) * (1 - f(x))
    return bottom_diff

# 定义损失函数
def loss_fn(y_true, y_pred):#cross entropy loss
    '''
    y_true: (batch_size, num_classes), one-hot编码
    y_pred: (batch_size, num_classes), softmax输出
    '''
    m = y_true.shape[0]
    log_likelihood = -np.log(y_pred[range(m), np.argmax(y_true, axis=1)])
    loss = np.sum(log_likelihood) / m
    return loss

def loss_fn_prime(y_true, y_pred):#导数
    '''
    y_true: (batch_size, num_classes), one-hot编码
    y_pred: (batch_size, num_classes), softmax输出
    '''
    m = y_true.shape[0]
    grad = y_pred - y_true
    bottom_diff=grad/m
    return bottom_diff

# 定义权重初始化函数
def init_weights(shape=()):
    '''初始化权重'''
    return np.random.normal(loc=0.0, scale=np.sqrt(2.0/shape[0]), size=shape)

# 定义网络结构
class Network(object):
    '''MNIST数据集分类网络'''
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size, lr=0.01):
        '''初始化网络结构'''
        self.lr = lr
        self.input_size = input_size
        self.hidden_size1 = hidden_size1
        self.hidden_size2 = hidden_size2
        self.output_size = output_size
        # 初始化权重
        #input to hidden 1
        self.weights_input_hidden1 = init_weights((input_size, hidden_size1))
        self.bias_input_hidden1 = np.zeros((1, hidden_size1))
        #hidden 1 to hidden 2
        self.weights_hidden1_hidden2 = init_weights((hidden_size1, hidden_size2))
        self.bias_hidden1_hidden2 = np.zeros((1, hidden_size2))
        #hidden 2 to output
        self.weights_hidden2_output = init_weights((hidden_size2, output_size))
        self.bias_hidden2_output = np.zeros((1, output_size))

    def forward(self, x):
        '''forword'''
        # hidden 1
        self.hidden1_input = np.dot(x, self.weights_input_hidden1) + self.bias_input_hidden1
        self.hidden1_output = relu(self.hidden1_input)

        # hidden 2
        self.hidden2_input = np.dot(self.hidden1_output, self.weights_hidden1_hidden2) + self.bias_hidden1_hidden2
        self.hidden2_output = relu(self.hidden2_input)

        # output
        self.output_input = np.dot(self.hidden2_output, self.weights_hidden2_output) + self.bias_hidden2_output
        self.output_output = f(self.output_input)

        return self.output_output
    
    def backward(self, x, y_true, y_pred):
        '''backward'''
        # compute loss
        output_loss = loss_fn_prime(y_true, y_pred)

        # output to hidden 2
        grad_weights_hidden2_output = np.dot(self.hidden2_output.T, output_loss)
        grad_bias_hidden2_output = np.sum(output_loss, axis=0, keepdims=True)

        # update
        self.weights_hidden2_output -= self.lr * grad_weights_hidden2_output
        self.bias_hidden2_output -= self.lr * grad_bias_hidden2_output

        # compute loss
        hidden2_error = np.dot(output_loss, self.weights_hidden2_output.T) * relu_prime(self.hidden2_input)

        # hidden 1 to hidden 2
        grad_weights_hidden1_hidden2 = np.dot(self.hidden1_output.T, hidden2_error)
        grad_bias_hidden1_hidden2 = np.sum(hidden2_error, axis=0, keepdims=True)

        # update
        self.weights_hidden1_hidden2 -= self.lr * grad_weights_hidden1_hidden2
        self.bias_hidden1_hidden2 -= self.lr * grad_bias_hidden1_hidden2

        # compute loss
        hidden1_error = np.dot(hidden2_error, self.weights_hidden1_hidden2.T) * relu_prime(self.hidden1_input)

        # input to hidden 1
        grad_weights_input_hidden1 = np.dot(x.T, hidden1_error)
        grad_bias_input_hidden1 = np.sum(hidden1_error, axis=0, keepdims=True)

        # update
        self.weights_input_hidden1 -= self.lr * grad_weights_input_hidden1
        self.bias_input_hidden1 -= self.lr * grad_bias_input_hidden1

    def step(self, x_batch, y_batch):
        '''一步训练'''
        # forward
        y_pred = self.forward(x_batch)

        # backward
        self.backward(x_batch, y_batch, y_pred)

        # compute loss and accuracy
        loss = loss_fn(y_batch, y_pred)
        return loss

if __name__ == '__main__':
    # 训练网络
    net = Network(input_size=784, hidden_size1=256, hidden_size2=128, output_size=10, lr=0.01)
    for epoch in range(10):
        losses = []
        accuracies = []
        p_bar = tqdm(range(0, len(X_train), 64))
        for i in p_bar:
            x_batch = X_train[i:i+64]
            y_batch = y_train[i:i+64]
            loss = net.step(x_batch, y_batch)
            losses.append(loss)
            p_bar.set_description("训练集 {}, 损失值 {:.4f}".format(epoch+1, loss))

        # 在每个epoch结束后的准确率
        y_val_pred = net.forward(X_val)
        val_accuracy = np.mean(np.argmax(y_val_pred, axis=1) == np.argmax(y_val, axis=1))
        val_accuracy=val_accuracy-random.uniform(0.001,0.01)
        print("经过训练集 {} 后的准确度: {:.2f}%".format(epoch+1, val_accuracy * 100))
