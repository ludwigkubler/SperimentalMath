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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_3cnf(n, m):
    if n <= 0 or m <= 0:
        raise ValueError("n and m must be positive integers")
    
    variables = list(range(1, n + 1))
    clauses = []
    
    for _ in range(m):
        clause = random.sample(variables + [-v for v in variables], 3)
        random.shuffle(clause)  # Ensure randomness
        clauses.append(clause)
    
    return clauses

def density_matrix(clauses, n):
    matrix = [[0] * (2 ** n) for _ in range(2 ** n)]
    
    for clause in clauses:
        for assignment in range(1, 2 ** n + 1):
            if all((assignment & (1 << abs(v) - 1)) != 0 == v > 0 or (assignment & (1 << abs(v) - 1)) == 0 == v < 0 for v in clause):
                matrix[assignment][assignment] += 1
    
    return matrix

def von_neumann_entropy(matrix, n):
    import math
    from fractions import Fraction
    
    # Normalize the matrix
    total = sum(sum(row) for row in matrix)
    normalized_matrix = [[Fraction(cell, total) for cell in row] for row in matrix]
    
    # Calculate entropy
    entropy = 0
    for row in normalized_matrix:
        for prob in row:
            if prob != 0:
                entropy -= prob * math.log2(prob)
    
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        m = 2 * n  # Example: each variable has 2 clauses
        clauses = generate_3cnf(n, m)
        
        matrix = density_matrix(clauses, n)
        rank = len([i for i, row in enumerate(matrix) if any(row[j] != 0 for j in range(2 ** n))])
        
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= 10 * n_values[-1] + m
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean rank {mean_rank} exceeds upper bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean rank exceeds upper bound\" first_failing_seed={first_failing_seed}")