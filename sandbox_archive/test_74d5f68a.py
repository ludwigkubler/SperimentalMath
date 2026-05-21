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
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i+1, m):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    return sum(1 for row in matrix if any(row))

def permanent(poly, n):
    if n == 0:
        return [1]
    result = []
    for i in range(len(poly)):
        new_poly = [poly[i]]
        for j in range(n-1):
            new_poly.append([sum(a*b for a, b in zip(p, q)) for p, q in zip(new_poly[-1], poly)])
        result.extend(new_poly)
    return result

def determinant(poly, n):
    if n == 0:
        return [1]
    result = []
    for i in range(len(poly)):
        new_poly = [poly[i]]
        for j in range(n-1):
            new_poly.append([sum(a*b for a, b in zip(p, q)) for p, q in zip(new_poly[-1], poly)])
        result.extend(new_poly)
    return result

def invariant_dimension(matrix, n):
    permanent_poly = permanent(matrix, n)
    determinant_poly = determinant(matrix, n)
    
    permanent_rank = gaussian_elimination(permanent_poly)
    determinant_rank = gaussian_elimination(determinant_poly)
    
    return permanent_rank - determinant_rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    supported_count = 0
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Test each n with 5 different matrices
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            permanent_rank = invariant_dimension(A, n)
            determinant_rank = invariant_dimension(A, n)
            
            if permanent_rank > determinant_rank:
                instances_tested += 1
                total_instances += 1
    
    conjecture_holds = instances_tested / len(n_values) >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Invariant Dimension Gap",
        "metric_value": (instances_tested / len(n_values)),
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")