import numpy as np
from netwon_method import netwon_methon
from bfgs import BFGS
"""
reference: 
李航《统计学习方法》
https://github.com/chenglu66/lr/blob/master/%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95
"""


# 2d rosenbrock function and its first and second order derivatives
# https://en.wikipedia.org/wiki/Rosenbrock_function
def rosenbrock(x):
    # x为列向量
    # 最小值出现在[1,1]处
    a = x[0][0]
    b = x[1][0]
    return 100 * (b - a**2)**2 + (1 - a)**2


def grad_rosen(x):
    a = x[0][0]
    b = x[1][0]
    return np.array([[200*(b-a**2)*(-2*a) + 2*(a-1)], [200*(b-a**2)]])


def hessian_rosen(x):
    a = x[0][0]
    b = x[1][0]
    # 矩阵是对称的
    return np.array([[1200*a**2 - 400*b + 2, -400*a], [-400*a, 200]])


if __name__ == '__main__':
    epsilon = 0.001
    x0 = [[0], [0]]
    # 牛顿法
    print('-----------------------------------')
    print('netwon_method')
    x = netwon_methon(x0, grad_rosen, hessian_rosen, epsilon)
    print("x", x, "result", rosenbrock(x))
    print('-----------------------------------')
    print('bfgs')
    x = BFGS(x0, rosenbrock, grad_rosen, epsilon)
    print("x", x, "result", rosenbrock(x))
