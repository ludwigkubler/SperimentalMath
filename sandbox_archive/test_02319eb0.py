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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(abs(x) != abs(y) for x, y in combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def frobenius_class(cnf):
        primes = set()
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    primes.add(literal)
                else:
                    primes.discard(abs(literal))
        return len(primes)
    
    def communication_complexity_rank_variance(truth_table):
        rank_variances = []
        for _ in range(100):  # Sample multiple representations
            permuted_truth_table = [truth_table[random.randint(0, len(truth_table) - 1)] for _ in truth_table]
            rank = sum(sum(row) > 0 for row in permuted_truth_table)
            rank_variances.append(rank)
        return statistics.variance(rank_variances)
    
    def C(n):
        return n
    
    results = []
    for n in range(5, 41):
        cnf = generate_cnf(n)
        frobenius_size = frobenius_class(cnf)
        rank_variance = communication_complexity_rank_variance(truth_table_from_cnf(cnf))
        results.append((n, frobenius_size, C(n) * rank_variance))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    n_values = [n for n, _, _ in results]
    frobenius_sizes = [frobenius_size for _, frobenius_size, _ in results]
    C_n_variances = [C(n) * rank_variance for _, _, rank_variance in results]
    
    correlation = pearson_correlation_coefficient(frobenius_sizes, C_n_variances)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.97 * statistics.stdev(C_n_variances),
        "counterexample": ""
    }

def pearson_correlation_coefficient(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_y2 = sum(yi ** 2 for yi in y)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
    
    return numerator / denominator if denominator != 0 else 0

def truth_table_from_cnf(cnf):
    n = max(abs(lit) for lit in cnf)
    truth_table = [[1] * (2 ** n) for _ in range(len(cnf))]
    for i, clause in enumerate(cnf):
        for literal in clause:
            if literal > 0:
                for j in range(2 ** n):
                    if not (j & (1 << (literal - 1))):
                        truth_table[i][j] = 0
            else:
                for j in range(2 ** n):
                    if j & (1 << (abs(literal) - 1)):
                        truth_table[i][j] = 0
    return truth_table

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = statistics.mean(result["metric_value"] for result in results)
        std_value = statistics.stdev(result["metric_value"] for result in results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")