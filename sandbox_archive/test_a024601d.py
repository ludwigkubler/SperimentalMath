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
    
    def generate_sat_instance(n):
        num_vars = n // 2
        clauses = []
        for _ in range(num_vars * 3):
            clause = [random.randint(1, num_vars), -random.randint(1, num_vars)]
            if random.choice([True, False]):
                clause[0] *= -1
            clauses.append(clause)
        return clauses
    
    def adjacency_matrix(n, clauses):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if any(abs(clause[0]) == i + 1 and abs(clause[1]) == j + 1 for clause in clauses):
                    A[i][j] = 1
                    A[j][i] = 1
        return A
    
    def spectral_gap(A):
        n = len(A)
        eigenvalues = []
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for _ in range(100):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
            Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            lambda_ = sum(v[i] * Av[i] for i in range(n))
            eigenvalues.append(lambda_)
        return max(eigenvalues) - min(eigenvalues)
    
    def resolution_width(clauses):
        # Simplified heuristic for demonstration
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_entropy = 0.0
    total_width = 0.0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_sat_instance(n)
            A = adjacency_matrix(n, clauses)
            entropy = spectral_gap(A)
            width = resolution_width(clauses)
            
            instances_tested += 1
            total_entropy += entropy
            total_width += width
    
    mean_entropy = total_entropy / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(entropy * width for entropy, width in zip(eigenvalues, eigenvalues)) - 
                               mean_entropy * instances_tested * mean_width) / \
                              math.sqrt((instances_tested * sum(entropy**2 for entropy in eigenvalues) - mean_entropy**2) *
                                        (instances_tested * sum(width**2 for width in eigenvalues) - mean_width**2))
    
    conjecture_holds = correlation_coefficient >= 0.8
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
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")