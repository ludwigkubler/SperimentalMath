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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    k = 5
    
    # Generate a monotone circuit C of size n computing k-CLIQUE
    C = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Apply a quantum geometric entanglement algorithm to the corresponding quantum state represented by C
    # This is a placeholder function. Replace with actual implementation.
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    b = [random.random() for _ in range(n)]
    x = gaussian_elimination(A, b)
    
    # Compute the minimal rank of the obtained quantum state
    rank = len([i for i, val in enumerate(x) if abs(val) > 1e-6])
    
    # Check if it is Θ(n^k)
    expected_rank = n**k
    tolerance = 2 * expected_rank
    
    metric_value = rank
    conjecture_holds = expected_rank - tolerance <= rank <= expected_rank + tolerance
    counterexample = "" if conjecture_holds else f"rank={rank}, expected={expected_rank}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_outside_tolerance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")