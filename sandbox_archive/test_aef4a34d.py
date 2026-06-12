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
    
    def gaussian_elimination(matrix, mod):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            pivot = matrix[i][i]
            for k in range(i+1, n):
                factor = (matrix[k][i] * pow(pivot, -1, mod)) % mod
                for j in range(i, n):
                    matrix[k][j] = (matrix[k][j] - factor * matrix[i][j]) % mod
        
        # Back substitution
        for i in range(n-1, -1, -1):
            pivot = matrix[i][i]
            for k in range(i-1, -1, -1):
                factor = (matrix[k][i] * pow(pivot, -1, mod)) % mod
                for j in range(n):
                    matrix[k][j] = (matrix[k][j] - factor * matrix[i][j]) % mod
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def tseitin_formula(G):
        n = len(G)
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        
        # Clause for each vertex
        for v in range(n):
            clause = [literals[v], literals[-v-1]]
            clauses.append(clause)
        
        # Clause for each edge
        for u in range(n):
            for v in G[u]:
                if u < v:
                    clause = [-literals[u], -literals[v], literals[-u-v-2]]
                    clauses.append(clause)
        
        return literals, clauses
    
    def resolution_width(clauses):
        queue = list(clauses)
        seen = set()
        width = 0
        
        while queue:
            new_clause = []
            for clause in queue:
                if any(lit < 0 and -lit in seen for lit in clause):
                    return float('inf')
                elif any(lit > 0 and lit not in seen for lit in clause):
                    new_clause.extend(clause)
                    seen.update(clause)
            
            if len(new_clause) > width:
                width = len(new_clause)
            
            queue.append(new_clause)
        
        return width
    
    def symplectic_form_matrix(G, mod):
        n = len(G)
        matrix = [[0] * (2*n) for _ in range(2*n)]
        
        # Identity block
        for i in range(n):
            matrix[i][i] = 1
            matrix[n+i][n+i] = 1
        
        # Adjacency block
        for u in range(n):
            for v in G[u]:
                if u < v:
                    matrix[u][v+n] = 1
                    matrix[v+n][u] = 1
        
        return matrix
    
    n = random.randint(5, 40)
    d = 3
    G = [[] for _ in range(n)]
    
    # Generate a random d-regular graph
    while any(len(G[u]) != d for u in range(n)):
        for u in range(n):
            neighbors = set(random.sample(range(n), d))
            while len(neighbors) < d:
                v = random.randint(0, n-1)
                if v not in G[u] and v != u:
                    neighbors.add(v)
            G[u] = list(neighbors)
    
    literals, clauses = tseitin_formula(G)
    matrix = symplectic_form_matrix(G, 2)
    sfr = gaussian_elimination(matrix, 2)
    w = resolution_width(clauses)
    
    return {
        "metric_name": "sfr_w_ratio",
        "metric_value": sfr / (w + 1e-9),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(sfr / w - 1) <= 0.2 * math.sqrt((sfr / w)**2 + (w / sfr)**2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_metric_value = 0
    count_conjecture_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_conjecture_holds += 1
    
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value)**2 for x in results) / len(results))
    support_fraction = count_conjecture_holds / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")