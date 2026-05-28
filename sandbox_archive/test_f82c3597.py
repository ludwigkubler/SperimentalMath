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

def gaussian_elimination(matrix, b):
    n = len(matrix)
    augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
    
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n + 1):
                augmented_matrix[j][k] += factor * augmented_matrix[i][k]
    
    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (augmented_matrix[i][-1] - sum(augmented_matrix[i][j] * x[j] for j in range(i+1, n))) / augmented_matrix[i][i]
    
    return x

def quandle_rank(edges):
    n = len(edges)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    rank = 0
    for i in range(n):
        if all(adjacency_matrix[i][j] == 0 for j in range(i)):
            continue
        rank += 1
        for j in range(n):
            if adjacency_matrix[j][i] != 0:
                for k in range(n):
                    adjacency_matrix[j][k] -= adjacency_matrix[i][k]
    
    return rank

def tseitin_formula(edges, n):
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    for u, v in edges:
        clauses.append([f'-{literals[u]}', f'{literals[v]}'])
        clauses.append([f'{literals[u]}', f'-{literals[v]}'])
        clauses.append([f'-{literals[u]}', f'-{literals[v]}', f'x{n+u+v}'])
        literals.append(f'x{n+u+v}')
    return clauses

def resolution_refutation_length(clauses):
    stack = [clauses]
    while stack:
        clause = stack.pop()
        if not clause:
            return len(stack)
        literal = next(l for l in clause if l[0] != '-')
        opposite_literal = f'-{literal}'
        new_clauses = []
        for c in stack:
            if opposite_literal in c:
                continue
            if literal in c:
                new_clauses.append([l for l in c if l != literal])
            else:
                new_clauses.append(c)
        stack.extend(new_clauses)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    edges = [(i, (i + j) % n) for i in range(n) for j in range(1, 4)]
    quandle_r = quandle_rank(edges)
    formula = tseitin_formula(edges, n)
    refutation_length = resolution_refutation_length(formula)
    
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2 ** quandle_r,
        "counterexample": "" if refutation_length >= 2 ** quandle_r else f"quandle_rank={quandle_r}, refutation_length={refutation_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r >= 2 ** quandle_r) / len(results)
    
    if all(r >= 2 ** quandle_r for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 2 ** quandle_r)
        print(f"RESULT: FALSIFIED counterexample='quandle_rank={quandle_r}, refutation_length={result}' first_failing_seed={first_failing_seed}")