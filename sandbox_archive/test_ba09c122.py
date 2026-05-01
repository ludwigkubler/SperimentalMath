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
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def generate_3sat_instance(n, m):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_rank = 0
        
        for _ in range(5):  # Sample 5 instances per n
            clauses = generate_3sat_instance(n, 3*n)
            incidence_matrix = [[int(v in clause) for v in range(1, n+1)] for clause in clauses]
            
            rank = gaussian_elimination(incidence_matrix)
            total_rank += rank
            instances_tested += 1
        
        avg_rank = total_rank / instances_tested
        conjecture_holds = False
        counterexample = ""
        
        if abs(avg_rank - math.log(n, 2)) < 0.5:
            conjecture_holds = True
    
    return {
        "metric_name": "rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested * len([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [int(math.log(p)) for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=unknown support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next(result for result in results if not result["conjecture_holds"])["counterexample"]
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")