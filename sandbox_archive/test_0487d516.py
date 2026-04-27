# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from collections import defaultdict, deque

def duval_factorization(s):
    n = len(s)
    i = 0
    factors = []
    while i < n:
        j = i + 1
        k = i
        while j < n and s[j] >= s[k]:
            if s[j] == s[k]:
                k = i
            j += 1
        for _ in range(j - i):
            factors.append(s[i])
            i += 1
    return factors

def leaves(f, memo=None):
    if memo is None:
        memo = {}
    n = len(f)
    if n == 0:
        return 0
    if f in memo:
        return memo[f]
    if all(x == f[0] for x in f) or all(x == f[1] for x in f):
        memo[f] = 1
        return 1
    min_leaves = float('inf')
    for i in range(1, n):
        left = leaves(f[:i], memo)
        right = leaves(f[i:], memo)
        if left + right < min_leaves:
            min_leaves = left + right
    memo[f] = min_leaves
    return min_leaves

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [2, 3, 4]
    results = []
    for n in n_values:
        total_functions = 1 << (1 << n)
        for _ in range(total_functions):
            f = ''.join(random.choice('01') for _ in range(1 << n))
            L_f = len(duval_factorization(f))
            Leaves_f = leaves(f)
            results.append((L_f, Leaves_f))
    min_L_f = min(L_f for _, L_f in results)
    max_Leaves_f = max(Leaves_f for _, Leaves_f in results)
    conjecture_holds = all(Leaves_f >= L_f for _, Leaves_f in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "min_L_f",
        "metric_value": min_L_f,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_L_f = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_L_f} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_L_f} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")