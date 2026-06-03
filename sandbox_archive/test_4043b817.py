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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    det = 0
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for c in range(n):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
    return det

def is_independent_set(graph, subset):
    n = len(graph)
    adjacency_matrix = [[graph[i][j] for j in range(n)] for i in range(n)]
    for u in subset:
        for v in subset:
            if u != v and adjacency_matrix[u][v] == 1:
                return False
    return True

def find_max_independent_set(graph):
    n = len(graph)
    max_size = 0
    max_set = []
    for i in range(1, 2**n):
        subset = [j for j in range(n) if (i & (1 << j))]
        if is_independent_set(graph, subset):
            if len(subset) > max_size:
                max_size = len(subset)
                max_set = subset
    return max_set

def betti_number(graph):
    n = len(graph)
    adjacency_matrix = [[graph[i][j] for j in range(n)] for i in range(n)]
    laplacian = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency_matrix[i])
        laplacian[i][i] = degree
        for j in range(i+1, n):
            laplacian[i][j] = -adjacency_matrix[i][j]
            laplacian[j][i] = -adjacency_matrix[j][i]
    
    # Find the rank of the Laplacian matrix
    rank = 0
    gaussian_elimination(laplacian)
    for row in laplacian:
        if any(row):
            rank += 1
    
    return rank

def resolution_width(cnf):
    n = len(cnf)
    clauses = [set(clause) for clause in cnf]
    variables = set()
    for clause in clauses:
        variables.update(clause)
    
    max_width = 0
    queue = list(variables)
    while queue:
        width = len(queue)
        if width > max_width:
            max_width = width
        
        new_queue = []
        for literal in queue:
            for clause in clauses:
                if literal in clause:
                    clause.remove(literal)
                    if not clause:
                        return -1
                    new_queue.extend(clause)
        
        queue = list(set(new_queue))
    
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnfs = []
        for _ in range(30):
            cnf = [[random.randint(-n, n) for _ in range(n)] for _ in range(n)]
            while not any(cnf[i][i] == 1 for i in range(n)):
                cnf = [[random.randint(-n, n) for _ in range(n)] for _ in range(n)]
            cnfs.append(cnf)
        
        total_diff = 0
        for cnf in cnfs:
            beta = betti_number(cnf)
            width = resolution_width(cnf)
            if width == -1:
                return {
                    "metric_name": "Betti Number vs Resolution Width",
                    "metric_value": None,
                    "instances_tested": len(cnfs),
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": "resolution_width returned -1"
                }
            total_diff += abs(beta - width)
        
        results.append({
            "n": n,
            "mean_diff": total_diff / len(cnfs)
        })
    
    mean_diff = sum(result["mean_diff"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["mean_diff"] - mean_diff) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Betti Number vs Resolution Width",
        "metric_value": mean_diff,
        "instances_tested": len(cnfs),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(result["mean_diff"] <= 10 for result in results),  # Assuming k = 10
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
    
    if all(trial["conjecture_holds"] for trial in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={sum(run_trial(seed)['metric_value'] for seed in seeds)/len(seeds)} std={math.sqrt(sum((run_trial(seed)['metric_value'] - sum(run_trial(seed)['metric_value'] for seed in seeds)/len(seeds))**2 for seed in seeds)/len(seeds))} support_fraction=1.0")
    elif any(not trial["conjecture_holds"] for trial in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed, trial in enumerate([run_trial(seed) for seed in seeds]) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_diff_exceeds_k\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")