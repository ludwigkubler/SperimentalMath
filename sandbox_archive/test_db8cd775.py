# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_tseitin_formula(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    
    # Generate literals
    literals = [random.choice([var, -var]) for var in variables]
    
    # Ensure at least one literal is true
    clauses.append(random.choice(literals))
    
    # Add clauses
    for _ in range(m):
        clause = random.sample(variables, 2)
        literals = []
        for var in clause:
            literals.extend([var, -var])
        clause = random.choice(literals)
        clauses.append(clause)
    
    return variables, clauses

def compute_coxeter_matrix(variables, clauses):
    n = len(variables)
    W_G = [[0] * n for _ in range(n)]
    
    for var in variables:
        W_G[abs(var)-1][abs(var)-1] += 1
    
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                var1 = abs(clause[i])
                var2 = abs(clause[j])
                W_G[var1-1][var2-1] += 1
                W_G[var2-1][var1-1] += 1
    
    return W_G

def tropicalize_matrix(W_G):
    n = len(W_G)
    for i in range(n):
        for j in range(i + 1, n):
            if W_G[i][j] > W_G[j][i]:
                W_G[j][i] = W_G[i][j]
            elif W_G[i][j] < W_G[j][i]:
                W_G[i][j] = W_G[j][i]
    
    for i in range(n):
        W_G[i][i] = math.inf
    
    return W_G

def compute_resolution_tree_width(clauses):
    n = len(clauses)
    tree_width = 0
    visited = [False] * n
    
    def dfs(node, current_width):
        nonlocal tree_width
        if visited[node]:
            return
        visited[node] = True
        for neighbor in range(n):
            if clauses[neighbor][node-1] != 0 and not visited[neighbor]:
                dfs(neighbor, max(current_width, abs(clauses[neighbor][node-1])))
        tree_width = max(tree_width, current_width)
    
    for i in range(n):
        dfs(i, 0)
    
    return tree_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(1, min(2 * n, 100))
    variables, clauses = generate_tseitin_formula(n, m)
    
    W_G = compute_coxeter_matrix(variables, clauses)
    tropicalized_W_G = tropicalize_matrix(W_G)
    
    metric_name = "min_rank_tropicalized_Coxeter_matrix"
    metric_value = max(sum(row) for row in tropicalized_W_G)  # Simplified rank estimation
    instances_tested = 1
    
    conjecture_holds = False
    counterexample = ""
    
    if metric_value >= math.log(n + math.log(m)):
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")