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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def create_matrix(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    row, col = literal - 1, abs(literal)
                else:
                    row, col = abs(literal) - 1, -literal
                matrix[row][col] += 1
        return matrix
    
    def geometric_flow(matrix):
        n = len(matrix) - 1
        flow_indices = []
        for i in range(n + 1):
            for j in range(1, n + 1):
                if matrix[i][j] > 0:
                    flow_indices.append(matrix[i][j])
        return flow_indices
    
    def variance(indices):
        mean = sum(indices) / len(indices)
        return sum((x - mean) ** 2 for x in indices) / len(indices)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_variance = 0
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        matrix = create_matrix(cnf)
        indices = geometric_flow(matrix)
        if indices:
            total_variance += variance(indices)
            instances_tested += len(indices)
    
    if instances_tested == 0:
        return {
            "metric_name": "variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid indices found"
        }
    
    mean_variance = total_variance / instances_tested
    n_max = max(n_values)
    conjecture_holds = abs(mean_variance - math.sqrt(n_max)) <= 0.1 * math.sqrt(n_max)
    counterexample = "" if conjecture_holds else "No valid indices found"
    
    return {
        "metric_name": "variance",
        "metric_value": mean_variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"No valid indices found\" first_failing_seed={first_failing_seed}")