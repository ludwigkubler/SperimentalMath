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
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for k in range(i+1, m):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for k in range(i+1, m):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] -= factor * A[i][j]
    return A

def is_sat(instance):
    m, n = len(instance), len(instance[0])
    A = [[Fraction(1) if instance[j][i] == '1' else Fraction(0) for i in range(n)] for j in range(m)]
    
    reduced_A = gaussian_elimination(A)
    
    # Check for contradictions
    for i in range(m):
        if reduced_A[i][-1] != 0:
            return False
    
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    
    instance = [[random.choice(['0', '1']) for _ in range(n)] for _ in range(m)]
    
    if not is_sat(instance):
        return {
            "metric_name": "log(m)",
            "metric_value": math.log(m),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_instance"
        }
    
    # Compute clause set complexity (number of clauses)
    c_phi = m
    
    return {
        "metric_name": "log(m)",
        "metric_value": math.log(m),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"unsatisfiable_instance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")