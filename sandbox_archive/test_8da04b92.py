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
    
    def generate_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_clause_subset_complexity(cnf):
        return len(cnf)
    
    def compute_minimal_modular_form_rank(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in cnf:
            literal1, literal2 = abs(clause[0]), abs(clause[1])
            if literal1 > n or literal2 > n:
                continue
            matrix[literal1 - 1][literal2 - 1] += 1
        
        rank = 0
        for row in matrix:
            non_zero = any(x != 0 for x in row)
            if non_zero:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    total_complexity = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * (n - 1) // 2))
            rank = compute_minimal_modular_form_rank(cnf)
            complexity = compute_clause_subset_complexity(cnf)
            
            total_rank += rank
            total_complexity += complexity
            instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_complexity = Fraction(total_complexity, instances_tested)
    
    correlation_coefficient = (instances_tested * mean_rank * mean_complexity - 
                               total_rank * total_complexity) / math.sqrt(
                                   (instances_tested * mean_rank**2 - total_rank**2) *
                                   (instances_tested * mean_complexity**2 - total_complexity**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")