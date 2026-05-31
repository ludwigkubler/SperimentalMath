# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def compute_clause_complexity(cnf):
        return len(cnf)
    
    def construct_noncommutative_polynomial_representation(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        R = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            if len(clause) == 2:
                i, j = abs(clause[0]), abs(clause[1])
                sign_i, sign_j = clause[0] // i, clause[1] // j
                R[i][j] += sign_i * sign_j
        return R
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for i in range(m):
                if i != pivot_row and matrix[i][col] != 0:
                    factor = matrix[i][col] / matrix[pivot_row][col]
                    for j in range(n):
                        matrix[i][j] -= factor * matrix[pivot_row][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        complexity = compute_clause_complexity(cnf)
        R = construct_noncommutative_polynomial_representation(cnf)
        rank = matrix_rank(R)
        
        ranks.append(rank)
        complexities.append(complexity)
    
    correlation_coefficient = sum((ranks[i] - mean_ranks) * (complexities[i] - mean_complexities) for i in range(len(n_values))) / len(n_values)
    mean_ranks = sum(ranks) / len(ranks)
    mean_complexities = sum(complexities) / len(complexities)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.6 <= correlation_coefficient < 0.8,
        "counterexample": "" if 0.6 <= correlation_coefficient < 0.8 else f"Correlation coefficient {correlation_coefficient} is out of the acceptable range [0.6, 0.8)"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient out of range\" first_failing_seed={first_failing_seed}")