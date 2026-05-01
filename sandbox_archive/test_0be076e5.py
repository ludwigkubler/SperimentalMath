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
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + matrix[i] for i, row in enumerate(matrix)]
        rows = list(range(m))
        cols = list(range(n))
        
        for col in cols:
            if all(row[col] == 0 for row in augmented_matrix):
                continue
            pivot_row = next(i for i, row in enumerate(augmented_matrix) if row[col] != 0)
            augmented_matrix[pivot_row], augmented_matrix[rows[0]] = augmented_matrix[rows[0]], augmented_matrix[pivot_row]
            rows[0], rows[i] = rows[i], rows[0]
            
            for i in range(1, m):
                factor = -augmented_matrix[i][col] / augmented_matrix[0][col]
                augmented_matrix[i] = [factor * a + b for a, b in zip(augmented_matrix[0], augmented_matrix[i])]
        
        return sum(1 for row in rows if any(row[col] != 0 for col in cols))
    
    def secant_variety_dimension(matrix):
        m, n = len(matrix), len(matrix[0])
        rank_2_flattening = []
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 1:
                    row = [matrix[x][y] * (x != i and y != j) for x in range(m) for y in range(n)]
                    rank_2_flattening.append(row)
        return rank(rank_2_flattening)
    
    dim_secant_variety = secant_variety_dimension(M)
    
    metric_name = "secant_variety_dimension"
    metric_value = dim_secant_variety
    instances_tested = 1
    conjecture_holds = dim_secant_variety >= n / 2
    counterexample = "" if conjecture_holds else f"dim(σ₂(V(M))) = {dim_secant_variety}, expected ≥ {n/2}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")