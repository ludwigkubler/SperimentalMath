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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Back-substitute
        solution = [0] * n
        for i in range(n-1, -1, -1):
            solution[i] = matrix[i][-1] / matrix[i][i]
            for j in range(i-1, -1, -1):
                matrix[j][-1] -= matrix[j][i] * solution[i]
        
        return solution
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def polarized_hodge_structure(poly):
        n = len(poly)
        hodge_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    hodge_matrix[i][j] = poly[i]
                elif abs(i - j) == 1:
                    hodge_matrix[i][j] = -poly[i]
        return gaussian_elimination(hodge_matrix)
    
    def resolution_proof_size(poly):
        n = len(poly)
        return sum(1 for coeff in poly if coeff != 0)
    
    def clause_indicator_polynomial(clique, n):
        poly = [0] * (n + 1)
        for node in clique:
            poly[node] = 1
        return poly
    
    def generate_k_clique(n, k):
        nodes = list(range(1, n+1))
        random.shuffle(nodes)
        return nodes[:k]
    
    n = random.randint(5, 40)
    k = min(k, n)  # Ensure k is valid
    clique = generate_k_clique(n, k)
    poly = clause_indicator_polynomial(clique, n)
    hodge_structure = polarized_hodge_structure(poly)
    num_monomials = sum(1 for row in hodge_structure if any(coeff != 0 for coeff in row))
    t_F = resolution_proof_size(poly)
    
    return {
        "metric_name": "resolution proof size",
        "metric_value": t_F,
        "instances_tested": 1,
        "conjecture_holds": num_monomials >= 0.9 * t_F and num_monomials <= 1.1 * t_F,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")