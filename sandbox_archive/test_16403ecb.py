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

def binom(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def sign(x):
    return 1 if x else -1

def S_f(f, n):
    Z = {}
    S = [[[0] * (n+1) for _ in range(n+1)] for _ in range(n+1)]
    for i in range(n + 1):
        for j in range(n + 1):
            for k in range(j + 1):
                if binom(n, i) * binom(i, k) * binom(n - i, j - k) > 0:
                    Z[(i, j, k)] = binom(n, i) * binom(i, k) * binom(n - i, j - k)
    for (i, j, k), z in Z.items():
        samples = min(200, z)
        count = 0
        for _ in range(samples):
            a = [random.randint(0, 1) for _ in range(i)]
            b = [random.randint(0, 1) for _ in range(j)]
            if len(set(a).intersection(b)) == k:
                count += sign(f(tuple(a), tuple(b)))
        S[i][j][k] = (count / z)
    return S

def kappa(f, n):
    S = S_f(f, n)
    U = []
    for i in range(n + 1):
        for j in range(n + 1):
            U.extend(S[i][j])
    U = [u for u in U if abs(u) > (1 / (n + 1)) ** 2]
    return len(U)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 10, 16, 24, 40]
    kappa_values = []
    for n in n_values:
        functions = [
            lambda x, y: all(x[i] == y[i] for i in range(n)),  # DISJ_n
            lambda x, y: any(x[i] != y[i] for i in range(n)),  # EQ_n
            lambda x, y: x[0] < y[0],  # GT_n (Alice<Bob)
            lambda x, y: random.random() > 0.5  # Random function
        ]
        kappa_values.extend([kappa(f, n) for f in functions])
    median_kappa_eq = sorted(kappa_values)[len(kappa_values) // 2]
    median_kappa_gt = sorted(kappa_values)[len(kappa_values) // 2 + len(n_values)]
    median_kappa_disj = sorted(kappa_values)[len(kappa_values) // 2 + 2 * len(n_values)]
    conjecture_holds = (median_kappa_eq <= 2 * math.log2(40) + 4 and
                        median_kappa_gt <= 2 * math.log2(40) + 4 and
                        median_kappa_disj / 40 >= 0.25)
    counterexample = "" if conjecture_holds else "median kappa(DISJ_n)/n < 0.25"
    return {
        "metric_name": "kappa",
        "metric_value": (median_kappa_eq + median_kappa_gt + median_kappa_disj) / 3,
        "instances_tested": len(kappa_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")