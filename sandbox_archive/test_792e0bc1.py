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

def binomial(n, k):
    if k > n:
        return 0
    res = 1
    for i in range(k):
        res *= (n - i)
        res //= (i + 1)
    return res

def colex_min(n, k):
    return binomial(n, k)

def shadow_defect(F, k):
    n = len(F[0])
    s_F = 0
    for comb in combinations(range(n), k-1):
        shadow = [any(all(F[i][j] == F[j][i] for j in range(k)) for i in comb) for _ in range(len(F))]
        s_F += sum(shadow)
    return s_F - colex_min(len(F), k-1)

def spectral_discrepancy(M_F):
    n = len(M_F)
    max_val = 0
    for x_vec in combinations([-1, 1], n):
        for y_vec in combinations([-1, 1], n):
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
                F = [tuple(random.sample(range(n), k)) for _ in range(size)]
                s_F = shadow_defect(F, k)
                M_F = [[1 if set(x) & set(y) == set() else -1 for y in F] for x in F]
                delta_F = spectral_discrepancy(M_F)
                R_F = delta_F * size * binomial(n, k-1) / max(s_F, 1)
                results.append((R_F, F))
    min_R, witness_F = min(results)
    conjecture_holds = min_R >= 0.125
    counterexample = "" if conjecture_holds else f"min(R)={min_R}, witness_F={witness_F}"
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
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.125) / len(results)
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean} std={std_dev} support_fraction={support_fraction}")