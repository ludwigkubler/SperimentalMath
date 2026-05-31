# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def compute_clause_complexity(cnf):
        return len(cnf)
    
    def noncommutative_polynomial_representation(cnf):
        n = max(abs(x) for x in sum(cnf, []))
        R = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            if len(clause) == 2:
                i, j = abs(clause[0]), abs(clause[1])
                sign_i = -1 if clause[0] < 0 else 1
                sign_j = -1 if clause[1] < 0 else 1
                R[i][j] += sign_i * sign_j
        return R
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i]):
                rank += 1
                for j in range(n):
                    if matrix[i][j]:
                        factor = Fraction(matrix[i][j], matrix[i][j])
                        for k in range(m):
                            matrix[k][j] -= factor * matrix[k][i]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        clause_complexity = compute_clause_complexity(cnf)
        R = noncommutative_polynomial_representation(cnf)
        rank_R = matrix_rank(R)
        
        results.append({
            "n": n,
            "clause_complexity": clause_complexity,
            "rank_R": rank_R
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ranks = [r["rank_R"] for r in results]
    complexities = [r["clause_complexity"] for r in results]
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    correlation_coefficient = pearson_correlation_coefficient(ranks, complexities)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.6 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results) / len(results)
    std_C = math.sqrt(sum((r["metric_value"] - mean_C) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(r["counterexample"] and float(r["counterexample"].split('=')[1]) < 0.6 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"] and float(r["counterexample"].split('=')[1]) < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")