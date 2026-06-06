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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def cnf_to_matrix(cnf, n):
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                var = abs(lit) - 1
                sign = 1 if lit > 0 else -1
                matrix[var][var] += sign
        return matrix
    
    def geometric_flow(matrix):
        n = len(matrix)
        flow_indices = []
        for i in range(n):
            for j in range(i + 1, n):
                diff = abs(matrix[i][j] - matrix[j][i])
                if diff > 0:
                    flow_indices.append(diff)
        return flow_indices
    
    def variance(indices):
        mean = sum(indices) / len(indices)
        return sum((x - mean) ** 2 for x in indices) / len(indices)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_variance = 0
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        matrix = cnf_to_matrix(cnf, n)
        indices = geometric_flow(matrix)
        if len(indices) > 0:
            total_variance += variance(indices)
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid indices found"
        }
    
    avg_variance = total_variance / instances_tested
    conjecture_holds = math.isclose(avg_variance, math.sqrt(n), rel_tol=1e-2)
    counterexample = "" if conjecture_holds else f"Variance {avg_variance} deviates from sqrt({n})"
    
    return {
        "metric_name": "variance",
        "metric_value": avg_variance,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Variance deviates from sqrt(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=All trials used n=1")