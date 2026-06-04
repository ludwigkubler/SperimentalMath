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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def local_induction_dimension(f):
        n = len(f)
        if n == 1:
            return 0
        dim = 1
        while True:
            found = False
            for i in range(n):
                for j in range(i+1, n):
                    if f[i] != f[j]:
                        new_f = [f[k] ^ (i < k < j) for k in range(n)]
                        if local_induction_dimension(new_f) == dim - 1:
                            found = True
                            break
                if found:
                    break
            if not found:
                return dim
            dim += 1
    
    def partial_commutative_matrix(f):
        n = len(f)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                M[i][j] = f[i] ^ f[j]
                M[j][i] = M[i][j]
        return M
    
    def matrix_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if all(M[j][i] == 0 for j in range(rank)):
                continue
            pivot_row = rank
            for j in range(pivot_row, n):
                if M[j][i] != 0:
                    break
            else:
                continue
            M[pivot_row], M[j] = M[j], M[pivot_row]
            for j in range(n):
                if j == pivot_row:
                    continue
                factor = M[j][i] / M[pivot_row][i]
                for k in range(i, n):
                    M[j][k] -= factor * M[pivot_row][k]
            rank += 1
        return rank
    
    def log_base_2(x):
        if x <= 0:
            return -math.inf
        return math.log2(x)
    
    n = random.randint(5, 30)
    f = generate_random_boolean_function(n)
    lnd_f = local_induction_dimension(f)
    M_f = partial_commutative_matrix(f)
    rank_M_f = matrix_rank(M_f)
    
    if lnd_f == 0:
        return {
            "metric_name": "ratio",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "lnd(f) is zero"
        }
    
    ratio = rank_M_f / (math.log(n, 2)**2 * lnd_f)
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")