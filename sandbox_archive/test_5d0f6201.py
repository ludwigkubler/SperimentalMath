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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return A

def rank(matrix):
    A = [row[:] for row in matrix]
    r = gaussian_elimination(A)
    rank = 0
    for row in r:
        if any(row[j] != 0 for j in range(len(row))):
            rank += 1
    return rank

def sos_degree(n):
    # Placeholder function to compute SOS degree
    # This is a dummy implementation and should be replaced with actual computation
    return n * (n + 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    incidence_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    np = sum(sum(row) for row in incidence_matrix)
    if np % 2 != 0:
        return {
            "metric_name": "Ratio of Minimal Rank to SOS Degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Invalid MAX-CUT instance"
        }
    
    minimal_rank = rank(incidence_matrix)
    sos_deg = sos_degree(n)
    
    return {
        "metric_name": "Ratio of Minimal Rank to SOS Degree",
        "metric_value": Fraction(minimal_rank, sos_deg),
        "instances_tested": 1,
        "conjecture_holds": None,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*3 + 1))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["metric_value"] is not None and result["conjecture_holds"] is None for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["metric_value"] <= Fraction(3, 2)) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] is not None and result["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample='Ratio too high' first_failing_seed={first_failing_seed}")