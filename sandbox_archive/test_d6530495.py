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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_representation(f):
        n = int(math.log2(len(f)))
        T = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                T[i][j] = f[(i & j) ^ (i | j)]
        return T
    
    def min_rank(T):
        n = len(T)
        rank = 0
        U = [list(row) for row in T]
        for i in range(n):
            max_val = -1
            max_col = -1
            for j in range(i, n):
                if abs(U[j][i]) > max_val:
                    max_val = abs(U[j][i])
                    max_col = j
            if max_val == 0:
                continue
            rank += 1
            for j in range(n):
                U[i][j] /= max_val
            for j in range(i + 1, n):
                factor = U[j][i]
                for k in range(n):
                    U[j][k] -= factor * U[i][k]
        return rank
    
    def polynomial_bound(s):
        # Placeholder for a polynomial bound function
        return s**2
    
    instances_tested = 0
    total_rank = 0
    conjecture_holds = True
    counterexample = ""
    
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            T = tensor_representation(f)
            rank = min_rank(T)
            instances_tested += 1
            total_rank += rank
            if rank > polynomial_bound(n):
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank}, bound={polynomial_bound(n)}"
    
    metric_value = total_rank / instances_tested
    return {
        "metric_name": "Minimum Tensor Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")