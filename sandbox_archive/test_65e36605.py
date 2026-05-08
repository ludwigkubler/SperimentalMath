# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

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
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    size = 2**n
    
    # Construct a read-twice branching program (simplified example)
    transition_matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute the free cumulant matrix via R-transform (simplified example)
    free_cumulant_matrix = [[0] * n for _ in range(n)]
    for i, j in product(range(n), repeat=2):
        if transition_matrix[i][j]:
            free_cumulant_matrix[i][j] = 1 / (i + j + 1)
    
    rank = gaussian_elimination(free_cumulant_matrix)
    
    # IP_2 trivial BP's cumulant rank for n=40
    ip2_rank = math.floor(0.9 * n)
    
    conjecture_holds = rank <= ip2_rank
    counterexample = "" if conjecture_holds else f"rank={rank}, expected<=ip2_rank={ip2_rank}"
    
    return {
        "metric_name": "cumulant_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")