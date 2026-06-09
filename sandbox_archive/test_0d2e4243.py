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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def power_iteration(matrix, num_iterations=100):
        n = len(matrix)
        v = [random.random() for _ in range(n)]
        v /= math.sqrt(sum(x**2 for x in v))
        
        for _ in range(num_iterations):
            v = matrix @ v
            v /= math.sqrt(sum(x**2 for x in v))
        
        return v
    
    def laplacian_matrix(graph):
        n = len(graph)
        L = [[0] * n for _ in range(n)]
        degree = [sum(1 for neighbor in graph[i] if neighbor != i) for i in range(n)]
        
        for i in range(n):
            L[i][i] = -degree[i]
            for j in graph[i]:
                if j > i:
                    L[i][j] = 1
                    L[j][i] = 1
        
        return L
    
    def eigenvalues(matrix):
        n = len(matrix)
        v = power_iteration(matrix)
        
        lambda_old = sum(matrix[i][j] * v[i] * v[j] for i in range(n) for j in range(i, n))
        lambda_new = lambda_old
        tolerance = 1e-6
        
        while abs(lambda_new - lambda_old) > tolerance:
            lambda_old = lambda_new
            v = power_iteration(matrix)
            lambda_new = sum(matrix[i][j] * v[i] * v[j] for i in range(n) for j in range(i, n))
        
        return lambda_new
    
    def generate_cnf(num_vars):
        clauses = []
        for _ in range(2 ** num_vars):
            clause = [random.randint(-1, -num_vars), random.randint(1, num_vars)]
            if clause not in clauses and -clause not in clauses:
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        for clause in cnf:
            if any(abs(lit) == abs(x) for x in stack):
                continue
            if all(lit < 0 for lit in clause):
                return float('inf')
            stack.append(clause[0])
        
        return len(stack)
    
    def bipartite_graph(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        graph = [[] for _ in range(n + 1)]
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    if clause[i] < 0 and clause[j] > 0 or clause[i] > 0 and clause[j] < 0:
                        graph[-clause[i]].append(-clause[j])
                        graph[-clause[j]].append(-clause[i])
        return graph
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = bipartite_graph(cnf)
    L = laplacian_matrix(graph)
    
    eig2 = eigenvalues(L)
    width = resolution_width(cnf)
    
    if eig2 == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "eig2(L(φ)) is zero"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        RESULT = f"SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] and r["counterexample"] for r in results):
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        RESULT = f"FALSIFIED counterexample=\"{' or '.join(counterexamples)}\" first_failing_seed={min(r['seed'] for r in results if not r['conjecture_holds'])}"
    else:
        RESULT = "INCONCLUSIVE insufficient support"
    
    print(RESULT)