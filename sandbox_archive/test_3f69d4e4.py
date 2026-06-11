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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def is_quaternion_compatible(poly, q):
        n = len(poly)
        matrix = [[0] * (n+1) for _ in range(n+1)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = poly[i] * q[j]
        return gaussian_elimination(matrix) != [[0] * (n+1)] * (n+1)

    def clause_indicator_polynomial(clauses):
        n = len(clauses)
        poly = [0] * (n + 1)
        for i in range(n):
            for j in range(2**i, 2**(i+1)):
                binary = bin(j)[3:]
                product = 1
                for k in range(len(binary)):
                    if binary[k] == '1':
                        product *= clauses[i][k]
                poly[j] += product
        return poly

    def resolution_width(clauses):
        n = len(clauses)
        width = [0] * (2**n)
        for i in range(n):
            for j in range(2**i, 2**(i+1)):
                binary = bin(j)[3:]
                product = 1
                for k in range(len(binary)):
                    if binary[k] == '1':
                        product *= clauses[i][k]
                width[j] += product
        return max(width)

    def minimal_quaternion_order(poly):
        n = len(poly)
        min_order = float('inf')
        for q in range(2**n):
            if is_quaternion_compatible(poly, q):
                min_order = min(min_order, q.bit_length())
        return min_order

    trials = 30
    instances_tested = 0
    n_max = 40
    total_correlation = 0

    for n in range(5, 41):
        if instances_tested >= trials:
            break
        
        clauses = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        poly = clause_indicator_polynomial(clauses)
        q_order = minimal_quaternion_order(poly)
        r_width = resolution_width(clauses)
        
        if q_order is not None and r_width is not None:
            correlation = q_order / r_width
            total_correlation += correlation
            instances_tested += 1
            n_max = max(n_max, n)

    mean_correlation = total_correlation / instances_tested if instances_tested > 0 else 0

    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_correlation >= 0.7 and all(correlation >= 0.5 for correlation in [total_correlation / instances_tested]),
        "counterexample": "" if mean_correlation >= 0.7 else "correlation < 0.5"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_correlation = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")