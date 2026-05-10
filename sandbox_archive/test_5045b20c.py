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

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = Fraction(M[j][i], M[i][i])
                for k in range(i, n+1):
                    M[j][k] -= factor * M[i][k]
    
    rank = 0
    for row in M:
        if any(row):
            rank += 1
    return rank

def discrepancy(clauses, variables):
    max_discrepancy = 0
    for S in range(1 << len(variables)):
        satisfied_clauses = sum(all(v in S for v in clause) for clause in clauses)
        max_discrepancy = max(max_discrepancy, abs(satisfied_clauses - len(clauses)))
    return max_discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    k = min(n // 2, 10)
    clauses = []
    for _ in range(k):
        clause = set(random.sample(range(n), random.randint(1, n)))
        clauses.append(clause)
    
    incidence_matrix = [[int(v in clause) for v in range(n)] for clause in clauses]
    
    rank = gaussian_elimination(incidence_matrix)
    discrepancy_value = discrepancy(clauses, range(n))
    
    expected_discrepancy = Fraction(1, rank)
    if discrepancy_value != expected_discrepancy:
        return {
            "metric_name": "discrepancy",
            "metric_value": discrepancy_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Discrepancy {discrepancy_value} does not match expected {expected_discrepancy}"
        }
    
    return {
        "metric_name": "discrepancy",
        "metric_value": discrepancy_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_discrepancy = sum(r["metric_value"] for r in results) / len(results)
    std_discrepancy = math.sqrt(sum((r["metric_value"] - mean_discrepancy)**2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_discrepancy} std={std_discrepancy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")