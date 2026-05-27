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
    
    def generate_symmetric_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                M[i][j] = random.randint(0, 1)
                M[j][i] = M[i][j]
        return M
    
    def symplectic_form(M):
        n = len(M)
        F = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i < n // 2 and j >= n // 2:
                    F[i][j] = M[i][j - n // 2]
                elif i >= n // 2 and j < n // 2:
                    F[i][j] = M[i - n // 2][j]
        return F
    
    def matrix_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if all(M[j][i] == 0 for j in range(rank)):
                continue
            rank += 1
            for j in range(i + 1, n):
                M[j][i], M[i][j] = M[i][j], M[j][i]
            for j in range(n):
                if j != i:
                    factor = M[j][i] / M[i][i]
                    for k in range(n):
                        M[j][k] -= factor * M[i][k]
        return rank
    
    def xor_and_tree_width(n):
        # This is a placeholder function. Implement the actual algorithm here.
        return n // 2
    
    def vector_space_dimension(k, n):
        return int(math.sqrt(n / k))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_symmetric_matrix(n)
    F = symplectic_form(M)
    rank_F = matrix_rank(F)
    expected_ratio = math.sqrt(n) / rank_F
    actual_ratio = rank_F / math.sqrt(n)
    
    xor_and_width = xor_and_tree_width(n)
    expected_dim = vector_space_dimension(k, n)
    actual_dim = int(math.sqrt(n / k))
    
    metric_name = "symplectic_form_rank_ratio"
    metric_value = actual_ratio
    instances_tested = 1
    conjecture_holds = abs(actual_ratio - expected_ratio) <= 0.1
    counterexample = "" if conjecture_holds else f"Ratio {actual_ratio} outside ±10% of {expected_ratio}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±10%\" first_failing_seed={first_failing_seed}")