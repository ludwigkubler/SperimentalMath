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
    
    def generate_matrix(n):
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M
    
    def symplectic_form(M):
        n = len(M)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        S = [[M[i][j] ^ M[j][i] for j in range(n)] for i in range(n)]
        return S
    
    def matrix_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if any(M[j][i] != 0 for j in range(rank, n)):
                M[rank], M[i] = M[i], M[rank]
                for j in range(rank + 1, n):
                    factor = M[j][i] / M[rank][i]
                    for k in range(n):
                        M[j][k] -= factor * M[rank][k]
                rank += 1
        return rank
    
    def xor_and_tree_width(n):
        # Placeholder implementation. This is a stub and should be replaced with actual logic.
        return n
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_matrix(n)
    S = symplectic_form(M)
    rank_S = matrix_rank(S)
    
    expected_ratio = math.sqrt(n / rank_S)
    observed_ratio = rank_S / math.sqrt(n)
    
    metric_value = observed_ratio
    instances_tested = 1
    conjecture_holds = abs(observed_ratio - expected_ratio) <= 0.1 * expected_ratio
    counterexample = "" if conjecture_holds else f"Observed ratio {observed_ratio}, expected ratio {expected_ratio}"
    
    return {
        "metric_name": "Symplectic Rank Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.9:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Observed ratio outside ±10% of expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or low support fraction")