# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(n=30):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_disjointness_matrix(n, seed=None):
    if seed is not None:
        random.seed(seed)
    M = [[0] * n for _ in range(n)]
    pairs = list(combinations(range(n), 2))
    random.shuffle(pairs)
    for i, (a, b) in enumerate(pairs[:n]):
        M[a][b] = M[b][a] = i + 1
    return M

def character_table(n):
    table = [[0] * n for _ in range(n)]
    table[0][0] = 1
    if n == 1:
        return table
    for k in range(1, n):
        for l in range(k + 1):
            sum_val = 0
            for j in range(l + 1):
                binom = math.comb(l, j)
                sign = (-1) ** (l - j)
                if k == l:
                    char_table_n_minus_k_l = 1 if j % 2 == 0 else 0
                else:
                    char_table_n_minus_k_l = character_table(n - k)[j][j]
                sum_val += sign * binom * char_table_n_minus_k_l
            table[k][l] = sum_val / math.sqrt(k + 1)
    return table

def fourier_coefficient(M, lambda_):
    n = len(M)
    char_table = character_table(n)
    chi_lambda = 0
    for i in range(n):
        for j in range(n):
            chi_lambda += M[i][j] * char_table[lambda_[i]][lambda_[j]]
    return abs(chi_lambda / (n ** 2))

def run_trial(seed: int) -> dict:
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = random_disjointness_matrix(n, seed)
    lambda_1 = [n - 1] + [1]
    lambda_n = [n]
    chi_lambda_1 = fourier_coefficient(M, lambda_1)
    chi_lambda_n = fourier_coefficient(M, lambda_n)
    metric_value = max(chi_lambda_1, chi_lambda_n)
    conjecture_holds = chi_lambda_1 >= n**2 / 2 and chi_lambda_n <= n / 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Fourier Coefficient Gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes()
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")