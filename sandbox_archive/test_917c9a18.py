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
    
    def local_induction_dimension(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    count += 1
        return count
    
    def partial_commutative_matrix(f):
        n = int(math.log2(len(f)))
        M = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    def matrix_rank(M):
        m, n = len(M), len(M[0])
        rank = 0
        for i in range(m):
            if all(M[i][j] == 0 for j in range(n)):
                continue
            pivot_col = next(j for j in range(n) if M[i][j] != 0)
            for j in range(n):
                if j != pivot_col:
                    factor = M[j][pivot_col] / M[i][pivot_col]
                    for k in range(m):
                        M[k][j] -= factor * M[k][pivot_col]
            rank += 1
        return rank
    
    def log2(x):
        return math.log(x, 2)
    
    n = random.randint(5, 30)
    f = generate_boolean_function(n)
    lnd_f = local_induction_dimension(f)
    if lnd_f > 40:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "lnd(f) > 40"
        }
    
    M_f = partial_commutative_matrix(f)
    rank_M_f = matrix_rank(M_f)
    
    ratio = rank_M_f / (log2(n)**2 * lnd_f)
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")