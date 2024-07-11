# 容错学习：Learning with Error
import numpy as np
import random


class LWE:
    def __init__(self, m: int, n: int, q: int, sigma: float):
        self.m = m  # 方程数量，越小求解越困难
        self.n = n  # 未知数个数，越大求解越困难
        self.q = q  # 素数，范围在[n^2, 2n^2]
        self.sigma = sigma  # 概率分布的方差

    def generate_random_matrix(self, m: int, n: int, uniform=True):
        # 生成随机矩阵
        if uniform:  # 需要均匀分布
            return np.random.randint(1, 9 + 1, (m, n))
        else:  # 不用均匀分布则默认正态分布
            return np.random.normal(0, self.sigma, (m, n))

    def generate_public_key(self):
        coefficient = self.generate_random_matrix(self.m, self.n)
        print(coefficient)
        variable = self.generate_random_matrix(self.n, 1)
        print(variable)
        error = self.generate_random_matrix(self.m, 1, False)
        print(error)
        value = np.dot(coefficient, variable)
        return value


# lwe = LWE(256, 640, 4093, 3.3)
lwe = LWE(6, 4, 29, 3.3)
pk = lwe.generate_public_key()
print(pk)


class RingLWE:
    def __init__(self, m, n, q, sigma):
        self.m = m  # 方程数量
        self.n = n  # 未知数个数
        self.q = q  # 素数
        self.sigma = sigma  # 概率分布的方差
