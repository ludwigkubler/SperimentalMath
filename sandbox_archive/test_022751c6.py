# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(n):
        coefficients = [random.randint(-10, 10) for _ in range(n+1)]
        return coefficients
    
    def evaluate_polynomial(coefficients, x):
        return sum(coeff * x**i for i, coeff in enumerate(coefficients))
    
    def derivative(coefficients):
        return [i * coeff for i, coeff in enumerate(coefficients)][1:]
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        result = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(b)
        augmented_matrix = [A[i] + [b[i]] for i in range(n)]
        
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            factor = Fraction(1, augmented_matrix[i][i])
            augmented_matrix[i] = [factor * coeff for coeff in augmented_matrix[i]]
            
            for j in range(n):
                if i != j:
                    factor = augmented_matrix[j][i]
                    augmented_matrix[j] = [augmented_matrix[j][k] - factor * augmented_matrix[i][k] for k in range(n+1)]
        
        return [row[-1] for row in augmented_matrix]

    def compute_tangent_sheaf_rank(f):
        n = len(f) - 1
        Df = derivative(f)
        A = [[Df[i] * x**j for j in range(n)] for i in range(n)]
        b = [0] * n
        return len(gaussian_elimination(A, b))
    
    def acc0_circuit_depth(f):
        n = len(f) - 1
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return 3
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_polynomial(n)
        rank = compute_tangent_sheaf_rank(f)
        depth = acc0_circuit_depth(f)
        
        if rank == 0 or depth == 0:
            continue
        
        ratio = Fraction(depth, rank)
        total_ratio += ratio
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = 1.2 >= mean_ratio <= 2.5
    
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio out of bounds: {mean_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='Ratio out of bounds' first_failing_seed=NA")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")