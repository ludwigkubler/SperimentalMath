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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = matrix[i][i]
        for j in range(i+1, n):
            matrix[j][i] /= factor
        
        # Eliminate above the pivot
        for j in range(i):
            factor = matrix[j][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def hodge_laplacian(phi, n, m):
    H = [[0] * (n+1) for _ in range(n+1)]
    for i in range(1, n+1):
        H[i][i-1] = 2
        H[i][i+1] = 2
        H[0][i] = -1
        H[n][i] = -1
    return H

def max_eigenvalue(matrix):
    n = len(matrix)
    eigenvalues = [matrix[i][i] for i in range(n)]
    return max(eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2*n)
            phi = [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
            
            Hodge_Laplacian = hodge_laplacian(phi, n, m)
            A = gaussian_elimination(Hodge_Laplacian)
            
            max_eig = max_eigenvalue(A)
            f_nm = m**(3/2) * n**(1/4)
            
            results.append({
                "n": n,
                "m": m,
                "max_eig": max_eig,
                "f_nm": f_nm
            })
    
    if not results:
        return {
            "metric_name": "max_eig",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    max_eigs = [result["max_eig"] for result in results]
    f_nms = [result["f_nm"] for result in results]
    mean_d = sum(max_eigs) / len(max_eigs)
    std_d = math.sqrt(sum((x - mean_d)**2 for x in max_eigs) / len(max_eigs))
    
    conjecture_holds = all(max_eig <= f_nm for max_eig, f_nm in zip(max_eigs, f_nms))
    counterexample = "" if conjecture_holds else "f(n,m) not satisfied"
    
    return {
        "metric_name": "max_eig",
        "metric_value": mean_d,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_d = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_d = math.sqrt(sum((x - mean_d)**2 for x in (result["metric_value"] for result in results if result["metric_value"] is not None)) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"f(n,m) not satisfied\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")