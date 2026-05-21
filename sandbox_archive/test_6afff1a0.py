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

def binomial(n, k):
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    result = 1
    for i in range(1, k + 1):
        result *= (n - i + 1)
        result //= i
    return result

def sign(x):
    return 1 if x else -1

def S_f(f, n, i, j, k):
    Z = binomial(n, i) * binomial(i, k) * binomial(n - i, j - k)
    if Z == 0:
        return 0
    count = 0
    for _ in range(min(200, Z)):
        a = [random.randint(0, 1) for _ in range(i)]
        b = [random.randint(0, 1) for _ in range(j)]
        if len(set(a).intersection(b)) == k:
            count += sign(f(tuple(a), tuple(b)))
    return Fraction(count, Z)

def kappa(f, n):
    S = [[S_f(f, n, i, j, k) for k in range(n + 1)] for j in range(n + 1)]
    singular_values = []
    for i in range(n + 1):
        row = [S[i][j] for j in range(n + 1)]
        col = [S[j][i] for j in range(n + 1)]
        max_val = max(abs(row), abs(col))
        if max_val > 0:
            singular_values.extend([max_val, 1 / (n + 1) ** 2])
    singular_values.sort(reverse=True)
    rank = sum(1 for sv in singular_values if sv > 1 / (n + 1) ** 2)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 10, 16, 24, 40]
    kappa_values = []
    
    def DISJ_n(x, y):
        return all(x[i] == y[i] for i in range(n))
    
    def EQ_n(x, y):
        return x == y
    
    def GT_n(x, y):
        return sum(x) > sum(y)
    
    functions = [DISJ_n, EQ_n, GT_n]
    
    for n in n_values:
        kappa_values.extend([kappa(f, n) for f in functions])
    
    metric_value = max(kappa_values)
    instances_tested = len(kappa_values)
    conjecture_holds = all(kv <= 2 * math.log2(n) + 4 for kv, n in zip(kappa_values[:len(n_values)], n_values)) and \
                       kappa_values[len(n_values):] >= [0.25 * n for n in n_values[2:]]
    
    return {
        "metric_name": "kappa_max",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["kappa_values"][len(n_values):] >= [0.25 * n for n in n_values[2:]] for r in results):
        print("RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")