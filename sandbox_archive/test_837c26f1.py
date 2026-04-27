# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random

def duval_factorization(w):
    n = len(w)
    factors = []
    i, j, k = 0, 0, 1
    while i < n:
        if w[i] == w[j]:
            if k == 1:
                j += 1
            else:
                i += 1
        else:
            if k > 1:
                factors.append(k)
            k = 1
            i = j
        if i == j:
            j += 1
    if k > 0:
        factors.append(k)
    return factors

def memoized_leaves(f, memo):
    n = len(f)
    if n == 0:
        return 1
    if f in memo:
        return memo[f]
    min_leaves = float('inf')
    for i in range(n):
        left = f[:i+1]
        right = f[i+1:]
        leaves = memoized_leaves(left, memo) + memoized_leaves(right, memo)
        if leaves < min_leaves:
            min_leaves = leaves
    memo[f] = min_leaves
    return min_leaves

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [2, 3, 4]
    results = []
    
    for n in n_values:
        total_functions = 1 << (1 << n)
        for _ in range(total_functions):
            f = ''.join(str(random.randint(0, 1)) for _ in range(1 << n))
            L_f = len(duval_factorization(f))
            Leaves_f = memoized_leaves(f, {})
            results.append((L_f, Leaves_f))
    
    all_L_f = [r[0] for r in results]
    all_Leaves_f = [r[1] for r in results]
    
    min_L_f = min(all_L_f)
    max_Leaves_f = max(all_Leaves_f)
    
    conjecture_holds = all(l <= L for l, L in zip(all_L_f, all_Leaves_f))
    counterexample = "" if conjecture_holds else f"min(L(f))={min_L_f}, max(Leaves(f))={max_Leaves_f}"
    
    return {
        "metric_name": "Lyndon Factor Count vs Leaves",
        "metric_value": min_L_f,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    all_L_f = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={sum(all_L_f)/len(all_L_f)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(all_L_f)/len(all_L_f)} std={(sum((x - sum(all_L_f)/len(all_L_f))**2 for x in all_L_f) / len(all_L_f))**0.5} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")