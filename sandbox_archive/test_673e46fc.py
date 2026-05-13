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

def generate_3sat_instance(n, clause_density):
    num_clauses = int(n * clause_density)
    literals = list(range(-n, 0)) + list(range(1, n+1))
    clauses = []
    for _ in range(num_clauses):
        clause = random.sample(literals, 3)
        clauses.append(clause)
    return clauses

def r_transform(matrix):
    n = len(matrix)
    if n == 0:
        return 0
    det = matrix[0][0]
    cofactor_matrix = [[matrix[i][j] for j in range(1, n)] for i in range(1, n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            det += (-1) ** (i + j) * matrix[i][j] * r_transform(minor)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    clause_density = 4.2
    instance = generate_3sat_instance(n, clause_density)
    
    # Construct the transition matrix (simplified for demonstration)
    transition_matrix = [[0] * (2**n) for _ in range(2**n)]
    for state in range(2**n):
        for literal in range(-n, n+1):
            if literal == 0:
                continue
            next_state = state ^ (1 << abs(literal)-1)
            transition_matrix[state][next_state] += 1
    
    # Compute the free cumulant sum via R-transform algorithm
    free_cumulant_sum = r_transform(transition_matrix)
    
    metric_name = "free_cumulant_sum"
    metric_value = abs(free_cumulant_sum)
    instances_tested = 1
    conjecture_holds = metric_value <= 0.9 * math.log(n) if instance else True
    counterexample = "" if conjecture_holds else f"hard_3sat_instance_with_clause_density_{clause_density}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"hard_3sat_instance_with_clause_density_{4.2}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")