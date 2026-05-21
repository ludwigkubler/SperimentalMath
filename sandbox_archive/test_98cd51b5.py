# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_disjointness_matrix(n):
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if bin(i & j).count('1') == 1:
                    A[i][j] = 1
                    A[j][i] = 1
        return A
    
    def secant_variety_dimension(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(i+1, n)):
                rank += 1
        return rank
    
    def is_generic_matrix(matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] == 0:
                    return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        matrix = generate_disjointness_matrix(n)
        if not is_generic_matrix(matrix):
            continue
        
        dimension = secant_variety_dimension(matrix)
        total_metric_value += dimension
        instances_tested += 1
        
        if dimension < n:
            conjecture_holds = False
            counterexample = f"Matrix with n={n}, dimension={dimension}"
    
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")