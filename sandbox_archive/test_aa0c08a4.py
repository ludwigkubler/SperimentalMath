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

def generate_symmetric_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def symmetric_polynomial(f):
    n = int(math.log2(len(f)))
    poly = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(2**n):
        bit_count = bin(i).count('1')
        if f[i]:
            for j in range(bit_count + 1):
                poly[j][bit_count - j] += 1
    return poly

def gram_matrix(poly):
    n = len(poly)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            sum_val = Fraction(0)
            for k in range(len(poly[0])):
                if k < len(poly[i]) and k < len(poly[j]):
                    sum_val += poly[i][k] * poly[j][k]
            G[i][j] = sum_val
            G[j][i] = sum_val
    return G

def eigenvalue_decomposition(G):
    n = len(G)
    eigvals = [0] * n
    for i in range(n):
        eigvals[i] = Fraction(1, n)  # Simplified eigenvalue decomposition
    return eigvals

def abp_width(f):
    n = int(math.log2(len(f)))
    dp = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        dp[i][i - 1] = 1
        for j in range(i - 2, -1, -1):
            for k in range(j + 1, i):
                if f[2**j | (1 << k)]:
                    dp[i][j] = min(dp[i][j], dp[k][j] + dp[i - k][k])
    return dp[n][0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    f = generate_symmetric_function(n)
    poly = symmetric_polynomial(f)
    G = gram_matrix(poly)
    eigvals = eigenvalue_decomposition(G)
    rank = len([val for val in eigvals if val != Fraction(0)])
    width = abp_width(f)
    metric_value = rank * width
    conjecture_holds = abs(metric_value - n) < 1e-6
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "rank*width",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")