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

def generate_tseitin_formula(n):
    if n <= 1:
        return []
    
    variables = list(range(1, 2 * n + 1))
    clauses = []
    
    for i in range(1, n + 1):
        var = variables[2 * i - 2]
        clause = [var, -variables[2 * i - 1]]
        clauses.append(clause)
        
        clause = [-var, variables[2 * i - 1]]
        clauses.append(clause)
    
    for i in range(1, n + 1):
        var = variables[2 * i - 2]
        clause = [variables[2 * i - 1]]
        for j in range(1, n + 1):
            if i != j:
                clause.append(-variables[2 * j - 2])
        clauses.append(clause)
    
    return clauses

def matrix_factorization(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                A[i][var - 1] += 1
            else:
                A[i][-var - 1] -= 1
    
    # Gaussian elimination to find the matrix factorization
    for i in range(n + 1):
        if A[i][i] == 0:
            return None, None
        
        for j in range(i + 1, n + 1):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]
    
    # Extract the matrix factorization
    U = [[0] * (n + 1) for _ in range(n + 1)]
    V = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                U[i][j] = A[i][i]
                V[j][i] = Fraction(1, A[i][i])
            else:
                U[i][j] = A[i][j + 1]
                V[j][i] = -A[j][i + 1] * Fraction(1, A[i][i])
    
    return U, V

def resolution_tree_width(clauses):
    n = len(clauses)
    tree = {}
    
    for i in range(n):
        tree[i] = set()
    
    for clause in clauses:
        if len(clause) == 2:
            var1, var2 = abs(clause[0]), abs(clause[1])
            tree[var1 - 1].add(var2 - 1)
            tree[var2 - 1].add(var1 - 1)
    
    visited = [False] * n
    queue = []
    
    for i in range(n):
        if not visited[i]:
            queue.append(i)
            visited[i] = True
    
    max_width = 0
    while queue:
        width = len(queue)
        max_width = max(max_width, width)
        
        new_queue = set()
        for node in queue:
            for neighbor in tree[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    new_queue.add(neighbor)
        
        queue = list(new_queue)
    
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_tseitin_formula(n)
    
    if not clauses:
        return {
            "metric_name": "Euler Characteristic vs. Resolution Tree Width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    U, V = matrix_factorization(clauses)
    if not U or not V:
        return {
            "metric_name": "Euler Characteristic vs. Resolution Tree Width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "matrix_factorization_failed"
        }
    
    euler_characteristic = sum(U[i][i] for i in range(n))
    resolution_width = resolution_tree_width(clauses)
    
    return {
        "metric_name": "Euler Characteristic vs. Resolution Tree Width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "conjecture_holds": resolution_width >= 2**(2 * euler_characteristic),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(30, 150, 5))
    
    results = []
    total_metric_value = 0
    count_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_holds += 1
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = count_holds / len(results)
    
    print("TRIALS:")
    for result in results:
        print(f"  TRIAL: {result}")
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")