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
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n + 1):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] += factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = A[i][n]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]

    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        s = 2**n
        coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
        
        A = [[coefficients[i] * j**k for k in range(n + 1)] for i in range(n + 1)]
        rank = 0
        
        # Perform Gaussian elimination to find the rank
        gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        
        results.append({
            "n": n,
            "s": s,
            "rank": rank,
            "conjecture_holds": abs(rank - math.log2(s)) <= 0.5
        })
    
    total_rank = sum(result["rank"] for result in results)
    avg_rank = total_rank / len(results)
    std_rank = (sum((result["rank"] - avg_rank) ** 2 for result in results) / len(results)) ** 0.5
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, s={results[0]['s']}, rank={results[0]['rank']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = (sum((result["metric_value"] - avg_rank) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, s={results[0]['s']}, rank={results[0]['rank']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")