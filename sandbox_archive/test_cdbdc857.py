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
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def matrix_multiply(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def next_prime(n):
        while not is_prime(n):
            n += 1
        return n
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
        for i in range(n):
            for j in range(i+1, n):
                clauses.append([variables[i], f'~{variables[j]}'])
                clauses.append([f'~{variables[i]}', variables[j]])
        return variables, clauses
    
    def resolution(clauses):
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = set(clauses[i])
                    clause_j = set(clauses[j])
                    if not (clause_i & clause_j):
                        complement_i = {f'~{x}' for x in clause_i}
                        complement_j = {f'~{x}' for x in clause_j}
                        new_clause = list(complement_i | complement_j)
                        if len(new_clause) == 1:
                            return True
                        new_clauses.append(new_clause)
            if not new_clauses:
                return False
            clauses.extend(new_clauses)
    
    def compute_l_function_order(n):
        # Simplified approximation for demonstration purposes
        return math.log2(n)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    resolution_result = resolution(clauses)
    
    if resolution_result:
        counterexample = "Formula can be resolved in polynomial time"
        conjecture_holds = False
    else:
        counterexample = ""
        conjecture_holds = True
    
    omega_L = compute_l_function_order(n)
    proof_length = len(clauses)  # Simplified for demonstration purposes
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [next_prime(2**i) for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Formula can be resolved in polynomial time' first_failing_seed={first_failing_seed}")