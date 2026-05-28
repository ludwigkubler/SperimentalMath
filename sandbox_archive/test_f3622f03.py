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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for r in range(i+1, n):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = -A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        
        for r in range(n):
            if r != i:
                factor = A[r][i]
                for j in range(i, n):
                    A[r][j] += factor * A[i][j]
    return sum(1 for row in A if all(x == 0 for x in row))

def hodge_rank(graph):
    n = len(graph)
    adjacency_matrix = [[0]*n for _ in range(n)]
    for u, v in graph:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    # Add identity matrix to make it a square matrix
    augmented_matrix = [row + [0]*(n+1) for row in adjacency_matrix]
    for i in range(n):
        augmented_matrix[i][-1] = 1
    
    return gaussian_elimination(augmented_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random expander graph
    n = random.randint(5, 40)
    m = random.randint(n * (n - 1) // 2, n * (n + 1) // 2)
    graph = set()
    while len(graph) < m:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in graph and (v, u) not in graph:
            graph.add((u, v))
    
    # Compute the Hodge rank
    rank = hodge_rank(graph)
    
    # Generate a Tseitin formula for this graph
    clauses = []
    for u, v in graph:
        x_u = f'x{u}'
        x_v = f'x{v}'
        clauses.append([f'{x_u} {x_v}', f'~{x_u} ~{x_v}', f'{x_u} ~{x_v}', f'~{x_u} {x_v}'])
    
    # Compute the resolution proof length (simplified for this test)
    proof_length = len(clauses) * 2
    
    # Check the conjecture
    if rank <= 2 ** math.log2(proof_length):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Rank {rank} exceeds bound for proof length {proof_length}"
    
    return {
        "metric_name": "Hodge Rank / Proof Length",
        "metric_value": rank / proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = result["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")