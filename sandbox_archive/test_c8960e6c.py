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
    
    n = 40
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    if any(sum(row) > 1 or sum(col) > 1 for row, col in zip(M, zip(*M))):
        return {
            "metric_name": "Noncommutative L^p norm",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "not_disjoint"
        }
    
    def matrix_norm(M, p):
        singular_values = []
        for i in range(n):
            row_sum = sum(abs(M[i][j]) for j in range(n))
            col_sum = sum(abs(M[j][i]) for j in range(n))
            if row_sum > 0:
                singular_values.append(row_sum ** (1 / p))
            if col_sum > 0:
                singular_values.append(col_sum ** (1 / p))
        return max(singular_values) ** (p - 1)
    
    min_norm = float('inf')
    for p in [1.5, 2, 2.5]:
        norm = matrix_norm(M, p)
        if norm < min_norm:
            min_norm = norm
    
    conjecture_holds = min_norm >= 0.1 * math.sqrt(n)
    counterexample = "" if conjecture_holds else "norm too small"
    
    return {
        "metric_name": "Noncommutative L^p norm",
        "metric_value": min_norm,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")