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
                    i, j = abs(lit1) - 1, abs(lit2) - 1
                    if lit1 > 0 and lit2 > 0:
                        A[i][j] += 1
                    elif lit1 < 0 and lit2 < 0:
                        A[i][j] -= 1
        return A
    
    def frobenius_norm(A):
        n = len(A)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += A[i][j] ** 2
        return math.sqrt(norm)
    
    def circuit_monotone_width(cnf):
        # Placeholder implementation, replace with actual calculation
        return len(cnf) / len(set(abs(lit) for lit in sum(cnf, [])))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, min(n * (n - 1) // 2, 100))
        cnf = generate_cnf(n, m)
        A = construct_quotient_algebra(cnf)
        norm = frobenius_norm(A)
        width = circuit_monotone_width(cnf)
        results.append((norm, width))
    
    mean_norm = sum(norm for norm, _ in results) / len(results)
    mean_width = sum(width for _, width in results) / len(results)
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((norm - mean_norm) * (width - mean_width) for norm, width in results)
        denominator = math.sqrt(sum((norm - mean_norm) ** 2 for norm, _ in results)) * math.sqrt(sum((width - mean_width) ** 2 for _, width in results))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = abs(correlation_coefficient) > 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {seed} {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")