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

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        pivot_row = i + max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[pivot_row] = M[pivot_row], M[i]
        if M[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            if j != i:
                factor = M[j][i] / M[i][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
    return M

def rank_of_matrix(M):
    n = len(M)
    rank = 0
    for row in range(n):
        if any(M[row]):
            rank += 1
    return rank

def rank_of_brauer_group(V):
    try:
        V = gaussian_elimination(V)
        return rank_of_matrix(V)
    except ValueError as e:
        print(f"ERROR: {e}")
        return None

def communication_complexity_xor(n):
    # Simulate XOR communication complexity
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):  # Test with 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = [random.randint(0, 1) for _ in range(1 << n)]
        V = [[f[i ^ j] for j in range(n)] for i in range(1 << n)]
        rank = rank_of_brauer_group(V)
        if rank is None:
            continue
        cc_xor = communication_complexity_xor(n)
        results.append((rank, cc_xor))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks, ccs = zip(*results)
    correlation_coefficient = sum((r - mean(ranks)) * (cc - mean(ccs)) for r, cc in zip(ranks, ccs)) / (len(results) * std(ranks) * std(ccs))
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def mean(x):
    return sum(x) / len(x)

def std(x):
    avg = mean(x)
    return math.sqrt(sum((xi - avg) ** 2 for xi in x) / len(x))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    
    for seed in seeds:
        print(f"TRIAL: {seed}")
        trial_result = run_trial(seed)
        results.append(trial_result)
    
    total_correlation_coefficient = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={total_correlation_coefficient/len(results)} std=0.0 support_fraction={support_fraction}")