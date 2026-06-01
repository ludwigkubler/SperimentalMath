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

def generate_sat_instance(n: int) -> list:
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        clauses.append(clause)
    return clauses

def polynomial_value(polynomial: dict, x_values: list) -> Fraction:
    result = Fraction(0)
    for term, coeff in polynomial.items():
        product = Fraction(1)
        for var, val in zip(term, x_values):
            if var != 0:
                product *= (val + 1) ** var
        result += coeff * product
    return result

def compute_minimal_local_ring_norm(polynomial: dict, n: int) -> Fraction:
    # Convert polynomial to matrix form for Gaussian elimination
    matrix = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
    for term, coeff in polynomial.items():
        row = [coeff]
        for var in term:
            if var != 0:
                row.extend([Fraction(1) if i == abs(var) - 1 else Fraction(0) for i in range(n)])
        matrix.append(row)
    
    # Gaussian elimination
    augmented_matrix = matrix[:]
    m, n = len(augmented_matrix), len(augmented_matrix[0])
    for i in range(m):
        if augmented_matrix[i][i] == 0:
            return Fraction(1)  # Singular matrix, norm is infinite
        for j in range(i + 1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Compute the minimal local ring norm
    norm = Fraction(0)
    for i in range(m):
        norm += abs(augmented_matrix[i][-1])
    return norm

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_sat_instance(n)
        polynomial = {}
        for clause in clauses:
            term = tuple(sorted(clause))
            if term not in polynomial:
                polynomial[term] = Fraction(1)
            else:
                polynomial[term] += Fraction(1)
        
        norm = compute_minimal_local_ring_norm(polynomial, n)
        results.append(norm)
    
    mean_norm = sum(results) / len(results)
    max_norm = max(results)
    conjecture_holds = all(norm <= 5 * math.sqrt(n) for norm, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else "norm_exceeds_bound"
    
    return {
        "metric_name": "minimal_local_ring_norm",
        "metric_value": mean_norm,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_norm = sum(result["metric_value"] for result in results) / len(results)
    std_norm = math.sqrt(sum((result["metric_value"] - mean_norm) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")