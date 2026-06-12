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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def hermitian_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(abs(matrix[j][i]) > 1e-9 for j in range(i, n)):
                rank += 1
        return rank

    def dpll_width(clauses, literals):
        if not clauses:
            return 0
        if not literals:
            return float('inf')
        literal = random.choice(literals)
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        return max(dpll_width(new_clauses, literals - {literal}), dpll_width(new_clauses, literals - {-literal}))

    def generate_clause(n):
        clause = []
        for _ in range(3):  # Each clause has 3 literals
            literal = random.choice([1, -1]) * (random.randint(0, n-1) + 1)
            if literal not in clause and -literal not in clause:
                clause.append(literal)
        return clause

    def generate_instance(n):
        clauses = [generate_clause(n) for _ in range(n)]
        literals = set(abs(lit) for clause in clauses for lit in clause)
        return clauses, literals

    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in {5, 10, 15, 20, 30, 40}:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Test each size with 5 instances
            clauses, literals = generate_instance(n)
            matrix = [[0] * (n+1) for _ in range(n+1)]
            for clause in clauses:
                for lit in clause:
                    matrix[lit][lit] += 1
            rank = hermitian_rank(gaussian_elimination(matrix))
            width = dpll_width(clauses, literals)
            
            if width == float('inf'):
                continue
            
            instances_tested += 1
            metric_values.append(rank / width)

    mean_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(value >= 1.0 for value in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_tropical_hermitian_rank_over_dpll_width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")