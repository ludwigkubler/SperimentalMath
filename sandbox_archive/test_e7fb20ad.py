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
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = 1 / matrix[i][i]
        for j in range(i, cols):
            matrix[i][j] *= factor
        for r in range(i+1, rows):
            factor = matrix[r][i]
            for j in range(i, cols):
                matrix[r][j] -= factor * matrix[i][j]
    
    # Eliminate above the pivot
    for i in range(rows-1, -1, -1):
        for r in range(i-1, -1, -1):
            factor = matrix[r][i]
            for j in range(i, cols):
                matrix[r][j] -= factor * matrix[i][j]
    
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def tseitin_formula(graph):
    n = len(graph)
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    
    # Each vertex must be connected to at least one other vertex
    for i in range(n):
        if not any(graph[i]):
            return None  # No edges, invalid graph
    
    # Create a Tseitin formula for the graph
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j]:
                clauses.append([f'x{i}', f'x{j}'])
                clauses.append([-f'x{i}', -f'x{j}'])
    
    # Ensure each vertex is connected to at least one other vertex
    for i in range(n):
        clause = [-literals[i]]
        for j in range(n):
            if graph[i][j]:
                clause.append(literals[j])
        clauses.append(clause)
    
    return literals, clauses

def symplectic_matrix(graph):
    n = len(graph)
    matrix = [[0] * (2*n) for _ in range(2*n)]
    
    # Fill the matrix with appropriate values
    for i in range(n):
        for j in range(n):
            if graph[i][j]:
                matrix[2*i][2*j+1] = 1
                matrix[2*i+1][2*j] = -1
    
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        if not any(any(row) for row in graph):
            continue
        
        literals, clauses = tseitin_formula(graph)
        if literals is None:
            continue
        
        matrix = symplectic_matrix(graph)
        rank = gaussian_elimination(matrix)
        
        resolution_length = len(clauses)
        ratio = rank / resolution_length if resolution_length > 0 else float('inf')
        
        results.append({
            "n": n,
            "rank": rank,
            "resolution_length": resolution_length,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Symplectic Rank / Resolution Proof Length",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graph found"
        }
    
    max_ratio = max(result["ratio"] for result in results)
    return {
        "metric_name": "Symplectic Rank / Resolution Proof Length",
        "metric_value": max_ratio,
        "instances_tested": len(results),
        "conjecture_holds": max_ratio >= 2**math.ceil(math.log(len(results), 2)),
        "counterexample": "" if max_ratio >= 2**math.ceil(math.log(len(results), 2)) else "max_ratio < 2^k for any k"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")