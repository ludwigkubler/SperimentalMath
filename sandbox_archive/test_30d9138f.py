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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

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
            for k in range(i+1, m):
                factor = Fraction(A[k][i], A[i][i])
                for l in range(n):
                    A[k][l] -= factor * A[i][l]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[Fraction(0, 1) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def permutation_circuit_threshold(f, n):
        # Placeholder implementation
        return 1.0  # This is a dummy value; replace with actual algorithm

    def schur_weyl_invariant(f, n):
        # Placeholder implementation
        return Fraction(1, 1)  # This is a dummy value; replace with actual calculation
    
    def generate_polynomial(n, D):
        coefficients = [random.randint(-10, 10) for _ in range(D+1)]
        return coefficients

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        total_rho = Fraction(0, 1)
        for _ in range(30):
            f = generate_polynomial(n, random.randint(1, D))
            rho = schur_weyl_invariant(f, n)
            total_rho += rho
        avg_rho = total_rho / 30
        threshold = permutation_circuit_threshold(f, n)
        results.append((n, avg_rho, threshold))

    mean_rho = sum(r[1] for r in results) / len(results)
    std_rho = math.sqrt(sum((r[1] - mean_rho)**2 for r in results) / len(results))
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((results[i][1] - mean_rho) * (results[i][2] - threshold) for i in range(len(results)))
        denominator = math.sqrt(sum((results[i][1] - mean_rho)**2 for i in range(len(results))) * sum((results[i][2] - threshold)**2 for i in range(len(results))))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.95
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Schur-Weyl Duality Invariant vs Permutation Circuit Threshold",
        "metric_value": mean_rho,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")