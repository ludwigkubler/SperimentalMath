# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from fractions import Fraction

def binomial(n, k):
    if k > n:
        return 0
    res = 1
    for i in range(k):
        res *= (n - i)
        res //= (i + 1)
    return res

def choose(l, k):
    if k == 0:
        return [[]]
    if len(l) < k:
        return []
    return [x[:k] for x in choose(l[1:], k-1)] + [[l[0]] + y for y in choose(l[1:], k-1)]

def sign_vector(x):
    return ''.join('+' if xi == 1 else '-' for xi in x)

def meet_in_the_middle(F, n):
    m = len(F)
    half = m // 2
    left = {sign_vector(x): sum(x) for x in choose(F[:half], half)}
    right = {sign_vector(x): sum(x) for x in choose(F[half:], half)}
    min_val = float('inf')
    for l, r in zip(left.values(), reversed(right.values())):
        if abs(l + r) < min_val:
            min_val = abs(l + r)
    return min_val

def kruskal_katona(n, k):
    if n == 0 or k == 0:
        return 0
    return binomial(n-1, k-1)

def shadow_defect(F, n, k):
    m = len(F)
    shadow = set()
    for i in range(m):
        for j in range(i+1, m):
            if sum(F[i][k-1] != F[j][k-1] for k in range(n)) == 1:
                shadow.add(tuple(sorted([i, j])))
    return len(shadow) - kruskal_katona(m, k-1)

def spectral_discrepancy(M_F):
    n = len(M_F)
    max_val = float('-inf')
    for x in itertools.product([-1, 1], repeat=n):
        x_vec = [x[i] for i in range(n)]
        for y in itertools.product([-1, 1], repeat=n):
            y_vec = [y[i] for i in range(n)]
            val = abs(sum(x_vec[i] * M_F[i][j] * y_vec[j] for j in range(n))) / n**2
            if val > max_val:
                max_val = val
    return max_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 11, 14]:
        for k in [2, 3, 4]:
            for size in range(binomial(n-1, k-1), binomial(n, k)+1):
                F = [tuple(random.choice([0, 1]) for _ in range(n)) for _ in range(size)]
                s_F = shadow_defect(F, n, k)
                M_F = [[1 if i == j else -1 if any(F[i][k-1] != F[j][k-1] for k in range(n)) else 0 for j in range(size)] for i in range(size)]
                delta_F = spectral_discrepancy(M_F)
                R_F = delta_F * size * binomial(n, k-1) / max(s_F, 1)
                results.append((R_F, F))
    min_R = min(R_F for R_F, _ in results)
    conjecture_holds = min_R >= Fraction(1, 8)
    counterexample = "" if conjecture_holds else str(results[0][1])
    return {
        "metric_name": "R(F)",
        "metric_value": min_R,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= Fraction(1, 8)) / len(results)
    if all(r >= Fraction(1, 8) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < Fraction(1, 8) for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < Fraction(1, 8)))]
        print(f"RESULT: FALSIFIED counterexample=\"{results[0][1]}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")