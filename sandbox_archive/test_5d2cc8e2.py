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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def binom(n, k):
    if k > n:
        return 0
    res = 1
    for i in range(k):
        res *= (n - i)
        res //= (i + 1)
    return res

def sign(x):
    return 1 if x else -1

def S_f(f, n):
    S = [[[0] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            Z = binom(n, i) * binom(i, j) * binom(n - i, j - i)
            if Z == 0:
                continue
            samples = min(Z, 200)
            for _ in range(samples):
                a = [random.randint(0, 1) for _ in range(i)]
                b = [random.randint(0, 1) for _ in range(j)]
                S[i][j][sum(a & set(b))] += sign(f(tuple(a), tuple(b)))
    return S

def kappa(f, n):
    S = S_f(f, n)
    U = []
    for i in range(n + 1):
        row = [S[i][j][k] for j in range(n + 1) for k in range(n + 1)]
        U.extend(row)
    U = [Fraction(x) for x in U]
    
    # Compute singular values via power iteration
    def matmul(A, B):
        return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]

    def svd_power_iteration(U, num_iterations=100):
        m = len(U)
        n = len(U[0])
        V = [[random.gauss(0, 1) / math.sqrt(n) for _ in range(m)] for _ in range(n)]
        for _ in range(num_iterations):
            U_V = matmul(U, V)
            V_UV = matmul(V, U_V)
            sigma = [sum(x * x for x in row)**0.5 for row in V_UV]
            V = [[x / s if s != 0 else 0 for x in row] for row, s in zip(V_UV, sigma)]
        return sigma

    singular_values = svd_power_iteration(U)
    threshold = Fraction(1, (n + 1)**2)
    kappa_value = sum(1 for s in singular_values if s > threshold)
    return kappa_value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def DISJ(x, y):
        return all(xi == yi for xi, yi in zip(x, y))
    
    def EQ(x, y):
        return x == y
    
    def GT(x, y):
        return any(xi > yi for xi, yi in zip(x, y))
    
    functions = [DISJ, EQ, GT]
    
    results = []
    for n in {6, 10, 16, 24, 40}:
        kappa_values = [kappa(f, n) for f in functions]
        results.append({
            "n": n,
            "kappa_DISJ": kappa_values[0],
            "kappa_EQ": kappa_values[1],
            "kappa_GT": kappa_values[2]
        })
    
    median_kappa_EQ = sorted([r["kappa_EQ"] for r in results])[len(results) // 2]
    median_kappa_GT = sorted([r["kappa_GT"] for r in results])[len(results) // 2]
    avg_kappa_DISJ_per_n = sum(r["kappa_DISJ"] / n for r in results if n >= 16) / len([r for r in results if n >= 16])
    
    conjecture_holds = median_kappa_EQ <= 2 * math.log2(40) + 4 and \
                       median_kappa_GT <= 2 * math.log2(40) + 4 and \
                       avg_kappa_DISJ_per_n >= 0.25
    
    return {
        "metric_name": "kappa",
        "metric_value": (median_kappa_EQ, median_kappa_GT, avg_kappa_DISJ_per_n),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "EQ or GT with kappa > 2*log(n)+4"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 10**6) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_kappa_EQ = sum(r["metric_value"][0] for r in results) / len(results)
        mean_kappa_GT = sum(r["metric_value"][1] for r in results) / len(results)
        avg_kappa_DISJ_per_n = sum(r["metric_value"][2] for r in results if r["n"] >= 16) / len([r for r in results if r["n"] >= 16])
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean_kappa_EQ={mean_kappa_EQ} mean_kappa_GT={mean_kappa_GT} avg_kappa_DISJ_per_n={avg_kappa_DISJ_per_n} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"EQ or GT with kappa > 2*log(n)+4\" first_failing_seed={r['seed']}")
                break