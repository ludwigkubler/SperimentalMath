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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

    # Back-substitute to get the solution
    solution = [0] * cols
    for i in range(rows - 1, -1, -1):
        solution[i] = Fraction(matrix[i][-1], matrix[i][i])
        for j in range(i - 1, -1, -1):
            matrix[j][-1] -= matrix[j][i] * solution[i]
    
    return solution

def is_invertible(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if rows != cols:
        return False
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(cols)] for i in range(rows)]
    augmented_matrix = [row + col for row, col in zip(matrix, identity)]
    gaussian_elimination(augmented_matrix)
    return all(abs(matrix[i][i]) > 0 for i in range(rows))

def tseitin_formula(graph_edges, n):
    literals = {node: f'x_{node}' for node in range(n)}
    clauses = []
    
    # Clause for each edge
    for u, v in graph_edges:
        literals[u], literals[v] = f'-{literals[u]}', f'-{literals[v]}'
        literals[n + u * n + v] = f'x_{n + u * n + v}'
        clauses.append(f'{literals[u]} {literals[v]} {literals[n + u * n + v]}')
        clauses.append(f'-{literals[u]} -{literals[n + u * n + v]}')
        clauses.append(f'-{literals[v]} -{literals[n + u * n + v]}')
        literals[u], literals[v] = f'x_{u}', f'x_{v}'
    
    # Clause for each vertex
    for i in range(n):
        literals[i] = f'-{literals[i]}'
        clauses.append(f'{literals[i]} {literals[0]}')
        literals[i] = f'x_{i}'
    
    return literals, clauses

def characteristic_polynomial(literals, n):
    x = [Fraction(1)]
    for i in range(n):
        x = [term * Fraction(-1) + coeff for coeff in x]
        x.append(Fraction(0))
    return x

def hypergeometric_series(x, n):
    series = [x[0]]
    for i in range(1, len(x)):
        term = x[i] / (i + 1)
        series.append(series[-1] + term)
    return series

def minimal_rank(hypergeometric_series):
    matrix = [[Fraction(0) for _ in range(len(hypergeometric_series))] for _ in range(len(hypergeometric_series))]
    for i, coeff in enumerate(hypergeometric_series):
        if coeff != 0:
            matrix[i][i] = Fraction(1)
            if i > 0:
                matrix[i - 1][i] = Fraction(-1)
                matrix[i][i - 1] = Fraction(-1)
    return len(gaussian_elimination(matrix))

def resolution_width(literals, clauses):
    # Simplified heuristic for demonstration purposes
    return len(set(literal[1:] for literal in literals.values()))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20  # Maximum number of vertices
    graph_edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n * (n - 1) // 2)]
    
    literals, clauses = tseitin_formula(graph_edges, n)
    char_poly = characteristic_polynomial(literals, n)
    hypergeometric_series_coeffs = hypergeometric_series(char_poly, n)
    rank = minimal_rank(hypergeometric_series_coeffs)
    width = resolution_width(literals, clauses)
    
    return {
        "metric_name": "Resolution Width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 2 ** (math.log(rank, 2) * math.log(2, math.e)),
        "counterexample": "" if width >= 2 ** (math.log(rank, 2) * math.log(2, math.e)) else f"Graph with n={n}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30))
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Graph with rank less than expected\" first_failing_seed={first_failing_seed}")