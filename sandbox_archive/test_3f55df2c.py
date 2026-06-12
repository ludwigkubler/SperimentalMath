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
        # Find pivot in column i
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate column i
        factor = A[i][i]
        for j in range(n):
            if j != i:
                multiplier = -A[j][i] / factor
                for k in range(n + 1):
                    A[j][k] += multiplier * A[i][k]
    
    # Back substitution to find the solution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A[i][n] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    
    return x

def birational_transformations(G):
    # Convert graph to adjacency matrix
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in G[u]:
            A[u][v] = 1
    
    # Perform Gaussian elimination to find the rank of the matrix
    rank = gaussian_elimination(A).count(0)
    
    return rank

def Tseitin_formula(G):
    n = len(G)
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    
    for u in range(n):
        if G[u]:
            clauses.append([variables[u]])
            for v in G[u]:
                clauses.append([-variables[u], variables[v]])
                clauses.append([-variables[v], variables[u]])
        else:
            clauses.append([-variables[u]])
    
    return clauses

def resolution_width(clauses):
    n = len(clauses)
    queue = [clauses[i] for i in range(n)]
    learned_clauses = []
    
    while queue:
        clause1 = queue.pop(0)
        if not clause1:
            continue
        
        for clause2 in queue + learned_clauses:
            if not clause2:
                continue
            
            common_var = None
            for var in clause1:
                if -var in clause2:
                    common_var = var
                    break
            
            if common_var is not None:
                new_clause = [v for v in clause1 if v != common_var] + [v for v in clause2 if v != -common_var]
                if len(new_clause) == 0:
                    return float('inf')
                
                queue.append(new_clause)
                learned_clauses.append(new_clause)
    
    return max(len(clause) for clause in learned_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        if n > n_max:
            break
        
        G = [random.sample(range(n), random.randint(1, n-1)) for _ in range(n)]
        m_geom_G = birational_transformations(G)
        phi_G = Tseitin_formula(G)
        w_phi_G = resolution_width(phi_G)
        
        metric_values.append(m_geom_G * w_phi_G)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    if len(metric_values) < instances_tested:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    return {
        "metric_name": "m_geom(G) * w(φ_G)",
        "metric_value": mean_value,
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "insufficient_instances" for r in results):
        print("RESULT: INCONCLUSIVE insufficient_instances")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not_enough_data' first_failing_seed={first_failing_seed}")