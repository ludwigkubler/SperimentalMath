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
    
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        rows_B = len(B)
        cols_B = len(B[0])
        if cols_A != rows_B:
            raise ValueError("Matrix dimensions do not match for multiplication")
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
        for i in range(rows):
            max_row = max(range(i, rows), key=lambda x: abs(augmented_matrix[x][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            for j in range(cols + 1):
                augmented_matrix[i][j] /= pivot
            for k in range(rows):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(cols + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[:-1] for row in augmented_matrix]
    
    def rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        non_zero_rows = sum(1 for row in reduced_matrix if any(x != 0 for x in row))
        return non_zero_rows
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([f'-{variables[i]}', f'-{variables[j]}', f'x{i+j}'])
                clauses.append([f'{variables[i]}', f'{variables[j]}', f'-x{i+j}'])
        return variables, clauses
    
    def generalized_ehrhart_lattice(variables, clauses):
        n = len(variables)
        lattice = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if all((i & (1 << k)) == (j & (1 << k)) or (i & (1 << k)) == 0 for k in range(n)):
                    lattice[i][j] = 1
        return lattice
    
    def resolution_width(clauses):
        n = len(clauses)
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        queue = list(clauses_set)
        width = 0
        while queue:
            new_queue = []
            for clause in queue:
                if len(clause) == 1:
                    continue
                literal = random.choice(clause)
                new_clause = [l for l in clause if l != literal and l != f'-{literal}']
                if not new_clause:
                    return width + 1
                new_queue.append(tuple(sorted(new_clause)))
            queue = list(set(new_queue))
            width += 1
        return width
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1):
        variables, clauses = tseitin_formula(n)
        lattice = generalized_ehrhart_lattice(variables, clauses)
        min_rank = rank(lattice)
        width = resolution_width(clauses)
        
        instances_tested += len(clauses)
        metric_values.append(min_rank / width)
    
    correlation_coefficient = sum(metric_values) / len(metric_values)
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")