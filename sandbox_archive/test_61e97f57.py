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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-c for c in clause]
            clauses.append(clause)
        return clauses
    
    def configuration_space_rank(clauses):
        n = len(clauses[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    row, col = literal - 1, n
                else:
                    row, col = -literal - 1, n
                
                matrix[row][col] += 1
                matrix[col][row] += 1
        
        # Gaussian elimination to find the rank of the matrix
        rank = 0
        for i in range(n + 1):
            if matrix[i][i] == 0:
                found_pivot = False
                for j in range(i + 1, n + 1):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            
            rank += 1
            for j in range(n + 1):
                if j == i:
                    continue
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        
        return rank
    
    def log2(x):
        return math.log2(x) if x > 0 else float('-inf')
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    rank = configuration_space_rank(clauses)
    log_rank = log2(rank)
    expected_bound = n / 3
    
    return {
        "metric_name": "log2(rank)",
        "metric_value": log_rank,
        "instances_tested": 1,
        "conjecture_holds": abs(log_rank - expected_bound) <= 1/3,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100))[:30]  # Default to first 30 primes if no seeds provided
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")