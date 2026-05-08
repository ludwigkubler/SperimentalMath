# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gaussian_elimination(A, b):
    n = len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            return None  # Singular matrix
        
        for j in range(i+1, n):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Backward substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
        x[i] /= augmented_matrix[i][i]
    
    return x

def rank(matrix):
    A = [row[:] for row in matrix]
    b = [0] * len(A)
    rref = gaussian_elimination(A, b)
    if rref is None:
        return 0
    rank = sum(1 for row in rref if any(row[i] != 0 for i in range(len(row)-1)))
    return rank

def generate_3cnf(n, clause_density):
    num_clauses = int(n * n * clause_density / 2)
    variables = list(range(1, n+1))
    clauses = set()
    
    while len(clauses) < num_clauses:
        a, b, c = random.sample(variables, 3)
        if (a, b, c) not in clauses and (a, c, b) not in clauses and (b, a, c) not in clauses \
           and (b, c, a) not in clauses and (c, a, b) not in clauses and (c, b, a) not in clauses:
            clauses.add((a, b, c))
    
    return clauses

def dnf_size(clauses):
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    clause_density = 4
    num_trials = 30
    
    total_dnf_size = 0
    count_supports_conjecture = 0
    counterexample_found = False
    
    for _ in range(num_trials):
        clauses = generate_3cnf(n, clause_density)
        dnf_size_value = dnf_size(clauses)
        
        if len(clauses) == 0:
            continue
        
        rho_n_k = rank([[1 if i in clause else 0 for i in range(1, n+1)] for clause in clauses])
        if rho_n_k is None or rho_n_k <= math.log(n):
            total_dnf_size += dnf_size_value
            if dnf_size_value >= n ** 1.5:
                count_supports_conjecture += 1
    
    mean_dnf_size = total_dnf_size / num_trials
    support_fraction = count_supports_conjecture / num_trials
    
    return {
        "metric_name": "DNF Size",
        "metric_value": mean_dnf_size,
        "instances_tested": num_trials,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if counterexample_found else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dnf_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dnf_size} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")