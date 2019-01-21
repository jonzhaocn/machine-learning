import numpy as np


def netwon_methon(x0, gradient_func, hesse_func, epsilon):
    """
    牛顿法
    :param x0: 输入初始值，列向量
    :param gradient_func: 目标函数的梯度
    :param hesse_func: 目标函数的海塞矩阵
    :param epsilon: 精度要求
    :return:
    """
    x = x0
    g = gradient_func(x)
    while np.linalg.norm(g) > epsilon:
        h = hesse_func(x)
        p = -np.dot(np.linalg.inv(h), g)
        x = x + p
        g = gradient_func(x)
    return x
