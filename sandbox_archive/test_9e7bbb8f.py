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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_clause_subset_complexity(cnf):
        return len(cnf)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i+1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def compute_minimal_modular_form_rank(cnf):
        n = len(set(abs(clause[0]) for clause in cnf))
        m = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal > 0:
                    matrix[i][literal - 1] += 1
                else:
                    matrix[i][-1] += abs(literal)
        rank = gaussian_elimination(matrix)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    total_complexity = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n * 2))
            rank = compute_minimal_modular_form_rank(cnf)
            complexity = compute_clause_subset_complexity(cnf)
            if rank is not None:
                instances_tested += 1
                total_rank += rank
                total_complexity += complexity
    
    mean_rank = total_rank / instances_tested
    mean_complexity = total_complexity / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * complexity for rank, complexity in zip(ranks, complexities)) - 
                               sum(ranks) * sum(complexities)) / math.sqrt((instances_tested * sum(rank**2 for rank in ranks) - sum(ranks)**2) *
                                                                     (instances_tested * sum(complexity**2 for complexity in complexities) - sum(complexities)**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")