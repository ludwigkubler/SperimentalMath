# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = -A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def mobius_function(L, T):
        if not T:
            return 1
        S = [s for s in L if s.issubset(T) and len(s) == len(T) - 1]
        return sum(-mobius_function(L, s) for s in S)

    def nw_design(d, n, k):
        S = []
        while len(S) < d:
            subset = set(random.sample(range(1, d + 1), n))
            if all(len(subset & s) <= k for s in S):
                S.append(subset)
        return S

    def nw_design_polynomial(d, n):
        p = 2
        x = [random.randint(0, p - 1) for _ in range(n)]
        y = [random.randint(0, p - 1) for _ in range(n)]
        z = [random.randint(0, p - 1) for _ in range(n)]
        return [[x[i] * y[j] + z[k] for k in range(n)] for i in range(n)]

    def walsh_transform(f):
        n = len(f)
        F = [[f[i ^ j] for j in range(1 << n)] for i in range(1 << n)]
        A = gaussian_elimination(F)
        return [sum(A[i][j] * (2 ** -n) for j in range(n)) for i in range(1 << n)]

    def nw_design_function(d, n, k):
        if random.random() < 0.5:
            return nw_design(d, n, k)
        else:
            return nw_design_polynomial(d, n)

    def compute_delta(D):
        L = []
        for i in range(1 << len(D)):
            T = {j + 1 for j in range(len(D)) if (i & (1 << j))}
            if all(len(T.intersection(s)) <= k for s in D):
                L.append(T)
        mu_L = {}
        for T in L:
            mu_L[T] = mobius_function(L, T)
        delta_D = sum(abs(mu_L[T]) * 2 ** -len(T) for T in L if T)
        return delta_D

    def compute_bias(D, f):
        m = len(D)
        bias = [0] * (1 << m)
        for y in range(1 << m):
            NW_D_f_y = [sum(f[i] * D[y & (1 << i)] for i in range(m)) % 2 for _ in range(1 << n)]
            for T in range(1, 1 << m):
                if T.bit_count() <= 4:
                    bias[T] += NW_D_f_y[random.randint(0, len(NW_D_f_y) - 1)]
        return [bias[T] / (1 << n) for T in range(1 << m)]

    def is_hard_function(f, delta_D):
        return any(abs(bias) > 4 * delta_D for bias in f)

    def compute_ols_slope(bias_values, delta_values):
        if not bias_values or not delta_values:
            return None
        log_bias = [math.log(abs(bias)) for bias in bias_values]
        log_delta = [math.log(delta) for delta in delta_values]
        n = len(log_bias)
        sum_log_bias = sum(log_bias)
        sum_log_delta = sum(log_delta)
        sum_log_bias_squared = sum(x * x for x in log_bias)
        sum_log_bias_log_delta = sum(x * y for x, y in zip(log_bias, log_delta))
        slope = (n * sum_log_bias_log_delta - sum_log_bias * sum_log_delta) / (n * sum_log_bias_squared - sum_log_bias ** 2)
        return slope

    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        n_values = [5, 8, 11, 14]
        d_values = range(8, 19)
        k = 2
        num_designs = 200
        num_hard_functions_per_design = 10
        
        results = []
        for n in n_values:
            for _ in range(num_designs):
                D = nw_design_function(d_values[seed % len(d_values)], n, k)
                delta_D = compute_delta(D)
                f = walsh_transform([random.randint(0, 1) for _ in range(2 ** n)])
                if is_hard_function(f, delta_D):
                    bias_values = compute_bias(D, f)
                    ols_slope = compute_ols_slope(bias_values, [delta_D] * len(bias_values))
                    results.append({
                        "metric_name": "OLS Slope",
                        "metric_value": ols_slope,
                        "instances_tested": 1,
                        "conjecture_holds": ols_slope is not None and ols_slope >= 0.5,
                        "counterexample": "" if ols_slope is not None else "mapping_undefined"
                    })
        
        mean_metric = sum(result["metric_value"] for result in results) / len(results)
        std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        return {
            "seed": seed,
            "mean_metric": mean_metric,
            "std_metric": std_metric,
            "support_fraction": support_fraction
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))