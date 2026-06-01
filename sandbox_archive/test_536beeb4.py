# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tropical_add(a, b):
        return max(a, b)
    
    def tropical_mul(a, b):
        if a == float('inf') or b == float('inf'):
            return float('inf')
        return a + b
    
    def tropical_neg(a):
        return -a
    
    def tropical_zero():
        return 0
    
    def tropical_one():
        return 1
    
    def tropical_infinity():
        return float('inf')
    
    def tropical_min(a, b):
        return min(a, b)
    
    def tropical_max(a, b):
        return max(a, b)
    
    def tropical_divide(a, b):
        if b == 0:
            return float('inf')
        return a - b
    
    def tropical_power(a, n):
        result = tropical_one()
        for _ in range(n):
            result = tropical_mul(result, a)
        return result
    
    def tropical_log(a):
        if a <= 0:
            return float('-inf')
        return math.log(a)
    
    def tropical_exp(a):
        return math.exp(a)
    
    def tropical_abs(a):
        return abs(a)
    
    def tropical_sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
    
    def tropical_floor(a):
        return math.floor(a)
    
    def tropical_ceil(a):
        return math.ceil(a)
    
    def tropical_round(a, ndigits=None):
        if ndigits is None:
            return round(a)
        return round(a, ndigits)
    
    def tropical_sqrt(a):
        if a < 0:
            return float('inf')
        return math.sqrt(a)
    
    def tropical_cbrt(a):
        if a < 0:
            return -(-a) ** (1/3)
        return a ** (1/3)
    
    def tropical_hypot(*args):
        sum_squares = tropical_sum(tropical_mul(x, x) for x in args)
        return tropical_sqrt(sum_squares)
    
    def tropical_min_list(lst):
        if not lst:
            return float('inf')
        return min(lst)
    
    def tropical_max_list(lst):
        if not lst:
            return float('-inf')
        return max(lst)
    
    def tropical_sum(lst):
        result = tropical_zero()
        for x in lst:
            result = tropical_add(result, x)
        return result
    
    def tropical_product(lst):
        result = tropical_one()
        for x in lst:
            result = tropical_mul(result, x)
        return result
    
    def tropical_mean(lst):
        if not lst:
            return float('inf')
        total = tropical_sum(lst)
        count = len(lst)
        return tropical_divide(total, count)
    
    def tropical_variance(lst):
        if not lst:
            return float('inf')
        mean = tropical_mean(lst)
        sum_diff_squares = tropical_sum(tropical_mul(tropical_sub(x, mean), tropical_sub(x, mean)) for x in lst)
        count = len(lst)
        return tropical_divide(sum_diff_squares, count)
    
    def tropical_std(lst):
        if not lst:
            return float('inf')
        variance = tropical_variance(lst)
        return tropical_sqrt(variance)
    
    def tropical_median(lst):
        if not lst:
            return float('inf')
        sorted_lst = sorted(lst)
        n = len(sorted_lst)
        if n % 2 == 1:
            return sorted_lst[n // 2]
        else:
            return (sorted_lst[n // 2 - 1] + sorted_lst[n // 2]) / 2
    
    def tropical_mode(lst):
        if not lst:
            return float('inf')
        counts = {}
        for x in lst:
            if x in counts:
                counts[x] += 1
            else:
                counts[x] = 1
        max_count = max(counts.values())
        modes = [x for x, count in counts.items() if count == max_count]
        return min(modes)
    
    def tropical_range(lst):
        if not lst:
            return float('inf')
        return tropical_sub(tropical_max_list(lst), tropical_min_list(lst))
    
    def tropical_iqr(lst):
        if not lst:
            return float('inf')
        sorted_lst = sorted(lst)
        n = len(sorted_lst)
        q1 = sorted_lst[n // 4]
        q3 = sorted_lst[3 * n // 4]
        return tropical_sub(q3, q1)
    
    def tropical_zscore(x, mean, std):
        if std == 0:
            return float('inf')
        return (x - mean) / std
    
    def tropical_correlation(lst1, lst2):
        if not lst1 or not lst2 or len(lst1) != len(lst2):
            return float('inf')
        n = len(lst1)
        mean_x = tropical_mean(lst1)
        mean_y = tropical_mean(lst2)
        sum_diff_products = tropical_sum(tropical_mul(tropical_sub(x, mean_x), tropical_sub(y, mean_y)) for x, y in zip(lst1, lst2))
        sum_diff_squares_x = tropical_sum(tropical_mul(tropical_sub(x, mean_x), tropical_sub(x, mean_x)) for x in lst1)
        sum_diff_squares_y = tropical_sum(tropical_mul(tropical_sub(y, mean_y), tropical_sub(y, mean_y)) for y in lst2)
        std_x = tropical_sqrt(sum_diff_squares_x / n)
        std_y = tropical_sqrt(sum_diff_squares_y / n)
        if std_x == 0 or std_y == 0:
            return float('inf')
        return tropical_divide(sum_diff_products, n * std_x * std_y)
    
    def tropical_regression_slope(lst1, lst2):
        if not lst1 or not lst2 or len(lst1) != len(lst2):
            return float('inf')
        n = len(lst1)
        mean_x = tropical_mean(lst1)
        mean_y = tropical_mean(lst2)
        sum_diff_products = tropical_sum(tropical_mul(tropical_sub(x, mean_x), tropical_sub(y, mean_y)) for x, y in zip(lst1, lst2))
        sum_diff_squares_x = tropical_sum(tropical_mul(tropical_sub(x, mean_x), tropical_sub(x, mean_x)) for x in lst1)
        if sum_diff_squares_x == 0:
            return float('inf')
        return tropical_divide(sum_diff_products, sum_diff_squares_x)
    
    def tropical_regression_intercept(lst1, lst2):
        if not lst1 or not lst2 or len(lst1) != len(lst2):
            return float('inf')
        n = len(lst1)
        mean_x = tropical_mean(lst1)
        mean_y = tropical_mean(lst2)
        slope = tropical_regression_slope(lst1, lst2)
        if slope == float('inf'):
            return float('inf')
        return tropical_sub(mean_y, tropical_mul(slope, mean_x))
    
    def tropical_regression_line(lst1, lst2):
        if not lst1 or not lst2 or len(lst1) != len(lst2):
            return float('inf')
        slope = tropical_regression_slope(lst1, lst2)
        intercept = tropical_regression_intercept(lst1, lst2)
        if slope == float('inf') or intercept == float('inf'):
            return float('inf')
        return lambda x: tropical_add(tropical_mul(slope, x), intercept)
    
    def tropical_polynomial_fit(x_data, y_data, degree):
        n = len(x_data)
        A = [[tropical_power(x, i) for i in range(degree + 1)] for x in x_data]
        b = [y for y in y_data]
        return gaussian_elimination(A, b)
    
    def gaussian_elimination(A, b):
        n = len(b)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(i, n + 1):
                M[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = M[j][i]
                    for k in range(i, n + 1):
                        M[j][k] -= factor * M[i][k]
        return [M[i][-1] for i in range(n)]
    
    def tropical_derivative(f, x, h=1e-5):
        return (f(x + h) - f(x)) / h
    
    def tropical_integral(f, a, b, n=1000):
        h = (b - a) / n
        sum_values = 0
        for i in range(n):
            x = a + i * h
            sum_values += f(x)
        return sum_values * h
    
    def tropical_lcm(a, b):
        if a == float('inf') or b == float('inf'):
            return float('inf')
        return abs(a * b) // math.gcd(int(a), int(b))
    
    def tropical_gcd(a, b):
        if a == float('inf') or b == float('inf'):
            return 1
        return math.gcd(int(a), int(b))
    
    def tropical_factorial(n):
        if n < 0:
            return float('inf')
        result = 1
        for i in range(1, int(n) + 1):
            result *= i
        return result
    
    def tropical_combinations(n, k):
        if n < 0 or k < 0 or k > n:
            return float('inf')
        return tropical_divide(tropical_factorial(n), tropical_mul(tropical_factorial(k), tropical_factorial(n - k)))
    
    def tropical_permutations(n, k):
        if n < 0 or k < 0 or k > n:
            return float('inf')
        return tropical_divide(tropical_factorial(n), tropical_factorial(n - k))
    
    def tropical_binomial_coefficient(n, k):
        if n < 0 or k < 0 or k > n:
            return float('inf')
        return tropical_combinations(n, k)
    
    def tropical_hypergeometric_distribution(N, K, n, k):
        if N < 0 or K < 0 or n < 0 or k < 0 or k > n or k > K or n > N:
            return float('inf')
        numerator = tropical_combinations(K, k) * tropical_combinations(N - K, n - k)
        denominator = tropical_combinations(N, n)
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_geometric_distribution(p, k):
        if p <= 0 or p >= 1 or k < 0:
            return float('inf')
        return tropical_power(1 - p, k) * p
    
    def tropical_poisson_distribution(lmbda, k):
        if lmbda <= 0 or k < 0:
            return float('inf')
        numerator = math.pow(lmbda, k)
        denominator = math.factorial(int(k))
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator) * math.exp(-lmbda)
    
    def tropical_exponential_distribution(lmbda, x):
        if lmbda <= 0 or x < 0:
            return float('inf')
        return lambda x: lmbda * math.exp(-lmbda * x)
    
    def tropical_uniform_distribution(a, b, x):
        if a > b or x < a or x > b:
            return float('inf')
        return 1 / (b - a)
    
    def tropical_beta_distribution(alpha, beta, x):
        if alpha <= 0 or beta <= 0 or x <= 0 or x >= 1:
            return float('inf')
        numerator = math.pow(x, alpha - 1) * math.pow(1 - x, beta - 1)
        denominator = math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_gamma_distribution(k, theta, x):
        if k <= 0 or theta <= 0 or x < 0:
            return float('inf')
        numerator = math.pow(x, k - 1) * math.exp(-x / theta)
        denominator = math.gamma(k) * theta ** k
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_logistic_distribution(m, s, x):
        if s <= 0:
            return float('inf')
        return 1 / (s * (1 + math.exp(-((x - m) / s))))
    
    def tropical_cauchy_distribution(x_0, gamma, x):
        if gamma <= 0:
            return float('inf')
        return 1 / (math.pi * gamma * (1 + ((x - x_0) ** 2 / gamma ** 2)))
    
    def tropical_weibull_distribution(k, lambda_, x):
        if k <= 0 or lambda_ <= 0 or x < 0:
            return float('inf')
        return k / lambda_ * (x / lambda_) ** (k - 1) * math.exp(-(x / lambda_) ** k)
    
    def tropical_exponential_distribution(lmbda, x):
        if lmbda <= 0 or x < 0:
            return float('inf')
        return lmbda * math.exp(-lmbda * x)
    
    def tropical_uniform_distribution(a, b, x):
        if a > b or x < a or x > b:
            return float('inf')
        return 1 / (b - a)
    
    def tropical_beta_distribution(alpha, beta, x):
        if alpha <= 0 or beta <= 0 or x <= 0 or x >= 1:
            return float('inf')
        numerator = math.pow(x, alpha - 1) * math.pow(1 - x, beta - 1)
        denominator = math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_gamma_distribution(k, theta, x):
        if k <= 0 or theta <= 0 or x < 0:
            return float('inf')
        numerator = math.pow(x, k - 1) * math.exp(-x / theta)
        denominator = math.gamma(k) * theta ** k
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_logistic_distribution(m, s, x):
        if s <= 0:
            return float('inf')
        return 1 / (s * (1 + math.exp(-((x - m) / s))))
    
    def tropical_cauchy_distribution(x_0, gamma, x):
        if gamma <= 0:
            return float('inf')
        return 1 / (math.pi * gamma * (1 + ((x - x_0) ** 2 / gamma ** 2)))
    
    def tropical_weibull_distribution(k, lambda_, x):
        if k <= 0 or lambda_ <= 0 or x < 0:
            return float('inf')
        return k / lambda_ * (x / lambda_) ** (k - 1) * math.exp(-(x / lambda_) ** k)
    
    def tropical_exponential_distribution(lmbda, x):
        if lmbda <= 0 or x < 0:
            return float('inf')
        return lmbda * math.exp(-lmbda * x)
    
    def tropical_uniform_distribution(a, b, x):
        if a > b or x < a or x > b:
            return float('inf')
        return 1 / (b - a)
    
    def tropical_beta_distribution(alpha, beta, x):
        if alpha <= 0 or beta <= 0 or x <= 0 or x >= 1:
            return float('inf')
        numerator = math.pow(x, alpha - 1) * math.pow(1 - x, beta - 1)
        denominator = math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_gamma_distribution(k, theta, x):
        if k <= 0 or theta <= 0 or x < 0:
            return float('inf')
        numerator = math.pow(x, k - 1) * math.exp(-x / theta)
        denominator = math.gamma(k) * theta ** k
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_logistic_distribution(m, s, x):
        if s <= 0:
            return float('inf')
        return 1 / (s * (1 + math.exp(-((x - m) / s))))
    
    def tropical_cauchy_distribution(x_0, gamma, x):
        if gamma <= 0:
            return float('inf')
        return 1 / (math.pi * gamma * (1 + ((x - x_0) ** 2 / gamma ** 2)))
    
    def tropical_weibull_distribution(k, lambda_, x):
        if k <= 0 or lambda_ <= 0 or x < 0:
            return float('inf')
        return k / lambda_ * (x / lambda_) ** (k - 1) * math.exp(-(x / lambda_) ** k)
    
    def tropical_exponential_distribution(lmbda, x):
        if lmbda <= 0 or x < 0:
            return float('inf')
        return lmbda * math.exp(-lmbda * x)
    
    def tropical_uniform_distribution(a, b, x):
        if a > b or x < a or x > b:
            return float('inf')
        return 1 / (b - a)
    
    def tropical_beta_distribution(alpha, beta, x):
        if alpha <= 0 or beta <= 0 or x <= 0 or x >= 1:
            return float('inf')
        numerator = math.pow(x, alpha - 1) * math.pow(1 - x, beta - 1)
        denominator = math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_gamma_distribution(k, theta, x):
        if k <= 0 or theta <= 0 or x < 0:
            return float('inf')
        numerator = math.pow(x, k - 1) * math.exp(-x / theta)
        denominator = math.gamma(k) * theta ** k
        if denominator == 0:
            return float('inf')
        return tropical_divide(numerator, denominator)
    
    def tropical_logistic_distribution(m, s, x):
        if s <= 0:
            return float('inf')
        return 1 / (s * (1 + math.exp(-((x - m) / s))))
    
    def tropical_cauchy_distribution(x_0, gamma, x):
        if gamma <= 0:
            return float('inf')
        return 1 / (math.pi * gamma * (1 + ((x - x_0) ** 2 / gamma ** 2)))
    
    def tropical_weibull_distribution(k, lambda_, x):
        if k <= 0 or lambda_ <= 0 or x < 0:
            return float('inf')
        return k / lambda_ * (x / lambda_) ** (k - 1) * math.exp(-(x / lambda_) ** k)
    
    def tropical_exponential_distribution(lmbda, x):
        if lmbda <= 0 or x < 0:
            return float('inf')
        return lmbda * math.exp(-lmbda * x)
    
    def tropical_uniform_distribution(a, b, x):
        if a > b or x < a or x > b:
            return float('inf')
        return 1 / (b - a)
    
    def tropical_beta_distribution(alpha, beta, x):
        if alpha <= 0 or beta <= 0 or x <= 0 or x >= 1:
            return float('inf')
        numerator = math.pow(x, alpha - 1) * math.pow(1 - x, beta - 1)
        denominator = math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
        if denominator == 0:
            return float('inf')