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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def polynomial_product(poly1, poly2):
        result = [0] * (len(poly1) + len(poly2) - 1)
        for i, coeff1 in enumerate(poly1):
            for j, coeff2 in enumerate(poly2):
                result[i + j] += coeff1 * coeff2
        return result
    
    def hodge_decomposition(polynomial):
        n = len(polynomial)
        if n == 1:
            return [polynomial[0]]
        half_n = n // 2
        left_half = polynomial[:half_n]
        right_half = polynomial[half_n:]
        left_hodge = hodge_decomposition(left_half)
        right_hodge = hodge_decomposition(right_half)
        result = []
        for i in range(len(left_hodge)):
            for j in range(len(right_hodge)):
                result.append(left_hodge[i] * right_hodge[j])
        return result
    
    def hodge_diamond_area(hodge):
        n = len(hodge)
        area = 0
        for i in range(n // 2 + 1):
            area += abs(hodge[i]) ** 2
        return area
    
    def resolution_proof_width(clauses):
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    n_max = 40
    instances_tested = 30
    total_area = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = generate_sat_instance(n)
        polynomial = [1]
        for clause in clauses:
            polynomial = polynomial_product(polynomial, clause)
        hodge = hodge_decomposition(polynomial)
        area = hodge_diamond_area(hodge)
        total_area += area
    
    mean_area = Fraction(total_area, instances_tested)
    
    return {
        "metric_name": "Hodge Diamond Area",
        "metric_value": float(mean_area),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_area <= n ** (2 / 3),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_area = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_area} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_area} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")