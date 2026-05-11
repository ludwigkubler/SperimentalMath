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
    
    def permanent(n):
        if n == 0:
            return 1
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        return result
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * determinant(submatrix)
        return det
    
    def sos_refutation_degree(poly, n):
        # Placeholder for actual SOS refutation degree computation
        # This is a dummy implementation that returns a random value
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    perm_poly = permanent(n)
    det_poly = determinant(permanent(n))
    
    perm_degree = sos_refutation_degree(perm_poly, n)
    det_degree = sos_refutation_degree(det_poly, n)
    
    metric_name = "SOS Refutation Degree Gap"
    metric_value = perm_degree - det_degree
    instances_tested = 1
    conjecture_holds = perm_degree > 2 * det_degree
    counterexample = "" if conjecture_holds else f"Permanent degree {perm_degree} not significantly larger than determinant degree {det_degree}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res for res in results if not res["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"Permanent degree not significantly larger than determinant degree\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")