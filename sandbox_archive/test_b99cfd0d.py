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
    
    def generate_cnf(n):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return " AND ".join(clauses)
    
    def matrix_mult(A, B, mod):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C
    
    def matrix_sub(A, B, mod):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C
    
    def gaussian_elimination(A, b, mod):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] = (A[i][j] * pow(pivot, -1, mod)) % mod
            b[i] = (b[i] * pow(pivot, -1, mod)) % mod
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] = (A[j][k] - factor * A[i][k]) % mod
                    b[j] = (b[j] - factor * b[i]) % mod
        return [b[i] for i in range(n)]
    
    def characteristic_polynomial(A, mod):
        n = len(A)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        char_poly = 1
        x = Fraction(0, 1)
        for k in range(1, n+1):
            A_k = matrix_mult(A, A**(k-1), mod)
            det_A_k = gaussian_elimination(A_k, [sum(row) % mod for row in identity], mod)[0]
            char_poly *= (x - det_A_k)
        return char_poly
    
    def resolution_width(phi):
        # Simplified version of resolution width calculation
        clauses = phi.split(" AND ")
        max_width = 0
        for clause in clauses:
            literals = clause.split(" OR ")
            max_width = max(max_width, len(literals))
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_cnf(n)
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        mod = random.randint(2, 100)
        
        char_poly = characteristic_polynomial(A, mod)
        width = resolution_width(phi)
        
        results.append({
            "n": n,
            "char_poly": char_poly,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    char_poly_values = [abs(result["char_poly"]) for result in results]
    width_values = [result["width"] for result in results]
    
    mean_char_poly = sum(char_poly_values) / len(char_poly_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((char_poly_values[i] - mean_char_poly) * (width_values[i] - mean_width) for i in range(len(results)))
        denominator = math.sqrt(sum((char_poly_values[i] - mean_char_poly)**2 for i in range(len(results))) * sum((width_values[i] - mean_width)**2 for i in range(len(results))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")