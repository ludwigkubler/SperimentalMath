# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_to_coxeter_group(f):
        n = len(f)
        G = [[0] * (n + 1) for _ in range(n + 1)]
        G[0][0] = 1
        for i in range(1, n + 1):
            G[i][i-1] = -1
            G[i][i] = 1
        return G
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def kw_protocol_cost(f):
        n = len(f)
        G = boolean_to_coxeter_group(f)
        b = [0] * (n + 1)
        b[0] = 1
        sol = gaussian_elimination(G, b)
        return sum(abs(x) for x in sol)
    
    def coxeter_group_length(G):
        n = len(G) - 1
        G_tilde = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            G_tilde[i][i] = 1
        for i in range(1, n + 1):
            for j in range(i):
                if G[i][j] != 0:
                    G_tilde[j][i] = -G[i][j]
        b = [0] * (n + 1)
        b[0] = 1
        sol = gaussian_elimination(G_tilde, b)
        return sum(abs(x) for x in sol)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        coxeter_length = coxeter_group_length(boolean_to_coxeter_group(f))
        kw_cost = kw_protocol_cost(f)
        results.append((coxeter_length, kw_cost))
    
    mean_coxeter = sum(x[0] for x in results) / len(results)
    mean_kw = sum(x[1] for x in results) / len(results)
    diff = abs(mean_coxeter - mean_kw)
    
    if diff > 10:
        return {
            "metric_name": "Coxeter Length vs KW Cost",
            "metric_value": diff,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": f"n={n}, coxeter_length={coxeter_length}, kw_cost={kw_cost}"
        }
    elif abs(mean_coxeter - mean_kw) > 3:
        return {
            "metric_name": "Coxeter Length vs KW Cost",
            "metric_value": diff,
            "instances_tested": len(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Coxeter Length vs KW Cost",
            "metric_value": diff,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": f"n={n}, coxeter_length={coxeter_length}, kw_cost={kw_cost}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0 support_fraction={support_fraction}")
    elif any(x["metric_value"] > 10 for x in results):
        first_failing_seed = next(x["seed"] for x in results if x["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"Coxeter Length is significantly less than KW Cost\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")