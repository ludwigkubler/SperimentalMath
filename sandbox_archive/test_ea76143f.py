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
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def construct_quotient_algebra(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        A = [[0] * n for _ in range(n)]
        for clause in cnf:
            for lit1 in clause:
                for lit2 in clause:
                    if lit1 != 0 and lit2 != 0:
                        A[abs(lit1) - 1][abs(lit2) - 1] += 1
        return A
    
    def frobenius_norm(A):
        n = len(A)
        sum_of_squares = 0
        for i in range(n):
            for j in range(n):
                sum_of_squares += A[i][j] ** 2
        return math.sqrt(sum_of_squares)
    
    def circuit_monotone_width(cnf):
        # Placeholder function, actual implementation needed
        return len(cnf)  # Simplified for testing purposes
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        m = random.randint(1, min(n * (n - 1), 100))  # Ensure m is reasonable
        cnf = generate_cnf(n, m)
        A = construct_quotient_algebra(cnf)
        norm = frobenius_norm(A)
        width = circuit_monotone_width(cnf)
        metrics.append((norm, width))
    
    if len(metrics) < 30:
        return {
            "metric_name": "Frobenius Norm vs Circuit Monotone Width",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_norm = sum(norm for norm, _ in metrics) / len(metrics)
    mean_width = sum(width for _, width in metrics) / len(metrics)
    expected_bound = 1.5 * math.sqrt(mean_width)
    
    if all(abs(norm - expected_bound) <= 0.5 * expected_bound for norm, _ in metrics):
        return {
            "metric_name": "Frobenius Norm vs Circuit Monotone Width",
            "metric_value": mean_norm,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Frobenius Norm vs Circuit Monotone Width",
            "metric_value": mean_norm,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Counterexample found: {mean_norm} not within 1.5 * sqrt({mean_width})"
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")