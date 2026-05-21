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
    n = random.choice([5, 10, 15, 20, 30, 40])
    s = 2 ** n
    
    # Generate a random polynomial of degree n
    coefficients = [random.randint(0, 10) for _ in range(n + 1)]
    
    # Construct the coefficient matrix (ABP)
    A = [[coefficients[i] * j**k for k in range(n + 1)] for i in range(n + 1)]
    
    # Compute the matroid rank using Gaussian elimination
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            max_row = None
            for row in range(rank, m):
                if matrix[row][col] != 0:
                    max_row = row
                    break
            if max_row is not None:
                matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
                for r in range(rank + 1, m):
                    factor = -matrix[r][col] / matrix[rank][col]
                    for c in range(n):
                        matrix[r][c] += factor * matrix[rank][c]
                rank += 1
        return rank
    
    matroid_rank = gaussian_elimination(A)
    
    # Check if the matroid rank scales as Θ(log s)
    expected_rank = math.log2(s) + 1
    tolerance = 0.5
    conjecture_holds = abs(matroid_rank - expected_rank) <= tolerance
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": matroid_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Expected rank ≈ {expected_rank}, got {matroid_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank does not scale as Θ(log s)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")