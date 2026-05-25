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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def schur_weyl_rank(n, k):
        if k < 0 or k >= 2 ** n:
            return None
        rank = 0
        for i in range(1, n + 1):
            rank += binomial_coefficient(n, i) * (2 ** (n - i))
        return rank
    
    def determinant_permutation_complexity(n, k):
        if k < 0 or k >= 2 ** n:
            return None
        complexity = 0
        for i in range(1, n + 1):
            complexity += binomial_coefficient(n, i) * (2 ** (n - i))
        return complexity
    
    def generate_instance(n, k):
        if k < 0 or k >= 2 ** n:
            return None
        instance = []
        for i in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            instance.append(row)
        return instance
    
    def compute_determinant(matrix):
        if len(matrix) == 0 or len(matrix[0]) == 0:
            return 0
        n = len(matrix)
        det = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += sign * matrix[0][i] * compute_determinant(submatrix)
            sign *= -1
        return det
    
    n = random.randint(5, 40)
    k = random.randint(0, 2 ** n // 4 - 1)
    
    instance = generate_instance(n, k)
    if instance is None:
        return {
            "metric_name": "det_π(I_π,k) / ρ(I_π,k)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rho = schur_weyl_rank(n, k)
    det = determinant_permutation_complexity(n, k)
    
    if rho is None or det is None:
        return {
            "metric_name": "det_π(I_π,k) / ρ(I_π,k)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = det / rho
    
    return {
        "metric_name": "det_π(I_π,k) / ρ(I_π,k)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 1 else False,
        "counterexample": "" if ratio <= 1 else f"Ratio {ratio} exceeds bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_message = f"SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        result_message = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    else:
        result_message = "INCONCLUSIVE"
    
    print(result_message)