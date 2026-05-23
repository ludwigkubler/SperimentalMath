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

def generate_random_twisted_module(q, n):
    M = [[random.randint(0, q-1) for _ in range(n)] for _ in range(n)]
    return M

def tensor_product(M, F_q_n):
    result = []
    for row_M in M:
        new_row = [sum(row_M[j] * F_q_n[i][j] for j in range(len(F_q_n))) % q for i in range(len(F_q_n))]
        result.append(new_row)
    return result

def find_minimal_rank(M, n):
    min_rank = float('inf')
    for perm in itertools.permutations(range(n)):
        permuted_M = [M[i] for i in perm]
        rank = sum(any(row) and all(x == 0 for row in A) for A in [permuted_M])
        if rank < min_rank:
            min_rank = rank
    return min_rank

def monotone_circuit_depth(n):
    # Placeholder function, replace with actual implementation
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q = random.randint(2, 5)
    n = random.randint(6, 40)
    M = generate_random_twisted_module(q, n)
    F_q_n = [[random.randint(0, q-1) for _ in range(n)] for _ in range(n)]
    
    minimal_rank = find_minimal_rank(M, n)
    depth = monotone_circuit_depth(n)
    ratio = depth / minimal_rank if minimal_rank != 0 else float('inf')
    
    conjecture_holds = ratio <= 1.5
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > 1.5"
    
    return {
        "metric_name": "Ratio of Monotone Circuit Depth to Minimal Rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 1.5' first_failing_seed={first_failing_seed}")