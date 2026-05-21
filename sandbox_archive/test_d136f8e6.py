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

def binomial(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 2
    for i in range(3, n + 1):
        result *= i
    return result

def choose(n, k):
    return binomial(n, k)

def sign(x):
    return -1 if x < 0 else 1

def S_f(f, n):
    S = [[[0 for _ in range(n+1)] for _ in range(n+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, n+1):
            Z = choose(n, i) * choose(i, j) * choose(n-i, j)
            if Z == 0:
                continue
            count = min(200, Z)
            for _ in range(count):
                a = [random.randint(0, 1) for _ in range(i)]
                b = [random.randint(0, 1) for _ in range(j)]
                S[i][j][sum(a & set(b))] += sign(f(tuple(a), tuple(b)))
    return S

def mode_1_unfolding(S):
    U = []
    for i in range(len(S)):
        for j in range(len(S[0])):
            row = [S[i][j][k] for k in range(len(S[0][0]))]
            U.append(row)
    return U

def singular_values(U):
    m, n = len(U), len(U[0])
    A = [[U[i][j] * U[i][j] for j in range(n)] for i in range(m)]
    for k in range(min(m, n)):
        max_val = 0
        for i in range(k, m):
            for j in range(k, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
        if max_val == 0:
            break
        for i in range(m):
            A[i][k] /= max_val
        for j in range(n):
            A[k][j] /= max_val
        for i in range(k+1, m):
            factor = A[i][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
        for j in range(k+1, n):
            factor = A[k][j]
            for i in range(m):
                A[i][j] -= factor * A[i][k]
    singulars = [math.sqrt(A[i][i]) for i in range(min(m, n))]
    return sorted(singulars)

def kappa(f, n):
    S = S_f(f, n)
    U = mode_1_unfolding(S)
    sigmas = singular_values(U)
    threshold = 1 / (n + 1) ** 2
    count = sum(1 for sigma in sigmas if sigma > threshold)
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 10, 16, 24, 40]
    results = []
    for n in n_values:
        kappa_disj = kappa(lambda x, y: all(xi == yi for xi, yi in zip(x, y)), n)
        kappa_eq = kappa(lambda x, y: x == y, n)
        kappa_gt = kappa(lambda x, y: sum(x) < sum(y), n)
        random_f = lambda x, y: random.choice([0, 1])
        kappa_random = kappa(random_f, n)
        results.append({
            "n": n,
            "kappa_disj": kappa_disj,
            "kappa_eq": kappa_eq,
            "kappa_gt": kappa_gt,
            "kappa_random": kappa_random
        })
    median_kappa_eq = sorted([r["kappa_eq"] for r in results])[len(results) // 2]
    median_kappa_gt = sorted([r["kappa_gt"] for r in results])[len(results) // 2]
    mean_kappa_disj_over_n = sum(r["kappa_disj"] / n for r in results if n >= 16) / len([r for r in results if n >= 16])
    conjecture_holds = median_kappa_eq <= 2 * math.log2(n_values[-1]) + 4 and \
                       median_kappa_gt <= 2 * math.log2(n_values[-1]) + 4 and \
                       mean_kappa_disj_over_n >= 0.25
    counterexample = "" if conjecture_holds else "median kappa_eq or kappa_gt too large"
    return {
        "metric_name": "kappa",
        "metric_value": (median_kappa_eq, median_kappa_gt, mean_kappa_disj_over_n),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    kappa_eq_values = [r["metric_value"][0] for r in results if "metric_value" in r]
    kappa_gt_values = [r["metric_value"][1] for r in results if "metric_value" in r]
    mean_kappa_disj_over_n_values = [r["metric_value"][2] for r in results if "metric_value" in r and r["instances_tested"] > 0]
    
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    mean_kappa_eq = sum(kappa_eq_values) / len(kappa_eq_values)
    std_kappa_eq = math.sqrt(sum((x - mean_kappa_eq) ** 2 for x in kappa_eq_values) / len(kappa_eq_values))
    mean_kappa_gt = sum(kappa_gt_values) / len(kappa_gt_values)
    std_kappa_gt = math.sqrt(sum((x - mean_kappa_gt) ** 2 for x in kappa_gt_values) / len(kappa_gt_values))
    mean_mean_kappa_disj_over_n = sum(mean_kappa_disj_over_n_values) / len(mean_kappa_disj_over_n_values)
    std_mean_kappa_disj_over_n = math.sqrt(sum((x - mean_mean_kappa_disj_over_n) ** 2 for x in mean_kappa_disj_over_n_values) / len(mean_kappa_disj_over_n_values))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean(kappa_eq)={mean_kappa_eq:.4f} std(kappa_eq)={std_kappa_eq:.4f} support_fraction={support_fraction:.2f}")
    elif any(r["conjecture_holds"] is False for r in results if "conjecture_holds" in r):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"median kappa_eq or kappa_gt too large\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction")