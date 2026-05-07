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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    if n == 2:
        a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
        return [(a + d) / 2 + math.sqrt(((a + d) / 2)**2 - (a * d - b * c)) / 2,
                (a + d) / 2 - math.sqrt(((a + d) / 2)**2 - (a * d - b * c)) / 2]
    e = [A[i][i] for i in range(n)]
    f = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                f[i][j] = A[i][j] / (e[i] - e[j])
    return [e[0]] + eigenvalues(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 15, 20, 25, 30, 35, 40]
    alpha_d = (1 / 2) * math.log(2)
    results = []
    
    for n in n_values:
        instances_tested = 0
        m_M_sum = 0
        m_M_min = float('inf')
        
        for _ in range(30):
            # Generate a 3-regular graph using the configuration model
            V = [i for i in range(n + 1)]
            E = []
            while len(E) < n:
                u, v = random.sample(V, 2)
                if (u, v) not in E and (v, u) not in E and u != v:
                    degree_u = sum(1 for e in E if e[0] == u or e[1] == u)
                    degree_v = sum(1 for e in E if e[0] == v or e[1] == v)
                    if degree_u < 3 and degree_v < 3:
                        E.append((u, v))
            
            # Assign odd parity charges
            b = [random.randint(0, 1) for _ in range(n + 1)]
            if sum(b) % 2 != 1:
                b[random.randint(0, n)] ^= 1
            
            # Construct the signed adjacency matrix A(G,b)
            A = [[0] * (n + 1) for _ in range(n + 1)]
            for u, v in E:
                A[u][v] = (-1) ** (b[u] + b[v])
            
            # Build the canonical degree-2 SOS moment matrix M(G,b)
            M = [[0] * (n + 1) for _ in range(n + 1)]
            M[0][0] = 1
            for i in range(1, n + 1):
                M[i][i] = 1
            for u, v in E:
                M[u][v] /= 2
                M[v][u] /= 2
            
            # Compute eigenvalues and spectral Mahler measure m(M)
            lambda_values = eigenvalues(M)
            m_M = sum(math.log(max(1, abs(lambda_val))) for lambda_val in lambda_values if abs(lambda_val) > 1)
            
            instances_tested += 1
            m_M_sum += m_M
            m_M_min = min(m_M_min, m_M)
        
        mean_m_M = m_M_sum / instances_tested
        slope, intercept, r_value, p_value, std_err = linear_regression(n_values, [mean_m_M] * len(n_values))
        
        results.append({
            "n": n,
            "instances_tested": instances_tested,
            "m_M_mean": mean_m_M,
            "m_M_min": m_M_min,
            "slope": slope,
            "intercept": intercept,
            "r_value": r_value,
            "p_value": p_value,
            "std_err": std_err
        })
    
    conjecture_holds = all(result["m_M_min"] >= alpha_d * result["n"] - 0.5 * math.log(result["n"]) for result in results)
    counterexample = "" if conjecture_holds else f"Instance with m(M) < {alpha_d * n_values[0] / 2}"
    
    return {
        "metric_name": "Spectral Mahler Measure",
        "metric_value": mean_m_M,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi ** 2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    r_value = (n * sum_xy - sum_x * sum_y) / math.sqrt((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
    p_value = 2 * (1 - abs(r_value))
    std_err = math.sqrt(1 - r_value ** 2) / math.sqrt(n - 2)
    
    return slope, intercept, r_value, p_value, std_err

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")