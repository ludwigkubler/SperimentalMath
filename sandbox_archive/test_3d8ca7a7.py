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
            clauses.append(clause)
        return clauses
    
    def term_overlap_matrix(cnf):
        n = len(cnf[0])
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for lit1 in clause:
                for lit2 in clause:
                    if abs(lit1) != abs(lit2):
                        matrix[abs(lit1) - 1][abs(lit2) - 1] += 1
        return matrix
    
    def alexander_brandt_index(matrix):
        n = len(matrix)
        total = sum(sum(row) for row in matrix)
        diagonal_sum = sum(matrix[i][i] for i in range(n))
        ab_index = (diagonal_sum / total) * (n - 1)
        return ab_index
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf[0])
        rank_variances = []
        for _ in range(30):  # Sample 30 different local-complexity distributions
            distribution = [random.randint(0, n) for _ in range(n)]
            rank = sum(distribution)
            rank_variances.append(rank ** 2)
        return sum(rank_variances) / len(rank_variances)
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    matrix = term_overlap_matrix(cnf)
    ab_index = alexander_brandt_index(matrix)
    rank_variance = communication_complexity_rank_variance(cnf)
    correlation_value = correlation([ab_index], [rank_variance])
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_value) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")