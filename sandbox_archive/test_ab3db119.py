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
    
    def hook_length(n, k):
        return (n - k + 1) * (n - k) // 2
    
    def young_diagram(m, n):
        diag = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            diag[i][i] = hook_length(i, 0)
            for j in range(1, min(i, n) + 1):
                diag[i][j] = diag[i - 1][j - 1] + hook_length(i, j)
        return diag
    
    def count_irreducible_components(diag):
        m, n = len(diag) - 1, len(diag[0]) - 1
        count = 0
        for i in range(m + 1):
            for j in range(n + 1):
                if diag[i][j] == 1:
                    count += 1
        return count
    
    def perm_matrix(n):
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            matrix[i][(i + 1) % n] = 1
        return matrix
    
    def det_matrix(n):
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i + j) % 2 == 0:
                    matrix[i][j] = 1
        return matrix
    
    def tensor_power(matrix, k):
        result = matrix
        for _ in range(1, k):
            result = [[sum(result[i][m] * matrix[m][j] for m in range(n)) for j in range(n)] for i in range(n)]
        return result
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        perm = perm_matrix(n)
        det = det_matrix(n)
        
        perm_tensor = tensor_power(perm, n)
        det_tensor = tensor_power(det, n)
        
        perm_diag = young_diagram(len(perm_tensor), len(perm_tensor[0]))
        det_diag = young_diagram(len(det_tensor), len(det_tensor[0]))
        
        perm_components = count_irreducible_components(perm_diag)
        det_components = count_irreducible_components(det_diag)
        
        results.append({
            "n": n,
            "perm_components": perm_components,
            "det_components": det_components
        })
    
    total_perm_components = sum(result["perm_components"] for result in results)
    total_det_components = sum(result["det_components"] for result in results)
    
    metric_value = total_perm_components / len(n_values)
    conjecture_holds = all(result["perm_components"] >= 2**(n/2) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Irreducible Components",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")