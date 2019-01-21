import numpy as np
from linear_search import find_step_length


def BFGS(x0, f_fun, gradient_func, epsilon):
    """
    BFGS算法
    :param x0: 目标方程的输入的初始值，列向量
    :param f_fun: 目标方程
    :param gradient_func: 目标方程的梯度
    :param epsilon: 精度
    :return:
    """
    x = x0
    # B为目标方程海塞矩阵的近似
    B = np.eye(len(x0))
    g = gradient_func(x)
    # 查看g的梯度是否小于精度，小于精度则不再计算
    if np.linalg.norm(g) < epsilon:
        return x
    while True:
        p = -np.dot(np.linalg.inv(B), g)
        # 使用一维搜索，查找lamda
        lamda = find_step_length(f_fun, gradient_func, x, 1.0, p, c2=0.9)
        x = x + lamda*p
        g_new = gradient_func(x)
        if np.linalg.norm(g_new) < epsilon:
            break
        y = g_new - g
        delta = lamda*p
        P = y.dot(y.T) / y.T.dot(delta)
        Q = -B.dot(delta).dot(delta.T).dot(B)/(delta.T.dot(B).dot(delta))
        B = B + P + Q
        g = g_new
    return x
