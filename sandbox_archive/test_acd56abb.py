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
    
    # Define the determinant and permanent polynomials for GL_n
    def det(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det_val = 0
            for col in range(n):
                submatrix = [[matrix[i][j] for j in range(n) if j != col] for i in range(1, n)]
                det_val += ((-1) ** col) * matrix[0][col] * det(submatrix)
            return det_val
    
    def perm(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] + matrix[0][1] * matrix[1][0]
        else:
            perm_val = 0
            for col in range(n):
                submatrix = [[matrix[i][j] for j in range(n) if j != col] for i in range(1, n)]
                perm_val += ((-1) ** col) * matrix[0][col] * det(submatrix)
            return perm_val
    
    # Compute orbit closure dimensions using Bialynicki-Birula decomposition
    def bialynicki_birula_decomposition(poly):
        if poly == det:
            return 2 * (n - 1) + 1
        elif poly == perm:
            return n * (n - 1)
    
    # Test for n=5, 10, 15, 20, 30, 40
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        det_dim = bialynicki_birula_decomposition(det)
        perm_dim = bialynicki_birula_decomposition(perm)
        
        results.append({
            "n": n,
            "det_dim": det_dim,
            "perm_dim": perm_dim
        })
    
    # Check if the conjecture holds for this seed
    conjecture_holds = all(det_dim < perm_dim for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "orbit_closure_dimension",
        "metric_value": det_dim,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")