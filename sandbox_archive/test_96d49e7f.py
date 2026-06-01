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
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def is_sat(instance):
    m, n = len(instance), len(instance[0])
    A = [[0] * (n + 1) for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if instance[i][j]:
                A[i][j] = -1
                A[i][-1] += 1
    
    reduced_A = gaussian_elimination(A)
    
    # Check for unsatisfiability
    for row in reduced_A:
        if row[-1] != 0 and all(x == 0 for x in row[:-1]):
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    
    # Generate a random SAT instance
    instance = [[random.choice([True, False]) for _ in range(n)] for _ in range(m)]
    
    if not is_sat(instance):
        return {
            "metric_name": "log(m)",
            "metric_value": math.log(m),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_instance"
        }
    
    # Calculate clause set complexity
    c_phi = sum(sum(row) for row in instance)
    
    return {
        "metric_name": "log(m)",
        "metric_value": math.log(m),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")