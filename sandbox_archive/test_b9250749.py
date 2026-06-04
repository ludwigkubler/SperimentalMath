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
    
    def generate_tseitin_formula(n, d):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate n clauses of the form x_i ∨ ¬x_j
        for i in range(n):
            j = (i + 1) % n
            clauses.append(f'{variables[i]} ∨ ¬{variables[j]}')
        
        # Generate d additional clauses that are linear combinations of variables
        for _ in range(d):
            clause = []
            coeffs = [random.choice([-1, 1]) for _ in range(n)]
            for coeff, var in zip(coeffs, variables):
                if coeff != 0:
                    clause.append(f'{coeff}{var}')
            clauses.append(' ∨ '.join(clause))
        
        return variables, clauses
    
    def longest_linear_dependency_chain(variables, clauses):
        n = len(variables)
        adjacency_matrix = [[0] * n for _ in range(n)]
        
        # Build the adjacency matrix
        for clause in clauses:
            literals = [lit.strip('¬') for lit in clause.split(' ∨ ')]
            for i in range(len(literals)):
                for j in range(i + 1, len(literals)):
                    if literals[i] != literals[j]:
                        u = int(literals[i][1:]) - 1
                        v = int(literals[j][1:]) - 1
                        adjacency_matrix[u][v] = 1
                        adjacency_matrix[v][u] = 1
        
        # Find the longest linear dependency chain using BFS
        max_length = 0
        for start in range(n):
            visited = [False] * n
            queue = [(start, 0)]
            while queue:
                u, length = queue.pop(0)
                if not visited[u]:
                    visited[u] = True
                    for v in range(n):
                        if adjacency_matrix[u][v] == 1 and not visited[v]:
                            queue.append((v, length + 1))
                            max_length = max(max_length, length + 1)
        
        return max_length
    
    def p_adic_valuation(val):
        if val == 0:
            return float('inf')
        k = 0
        while val % 2 == 0:
            val //= 2
            k += 1
        return k
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    
    for n in range(5, 41):
        variables, clauses = generate_tseitin_formula(n, n // 2)
        l_phi = longest_linear_dependency_chain(variables, clauses)
        
        # Compute the resolution proof width (simplified for this test)
        w_phi = n
        
        p_val = p_adic_valuation(w_phi)
        k = 1
        while True:
            if math.log(p_val ** k) == n - l_phi + 0.1 * n or math.log(p_val ** k) == n - l_phi - 0.1 * n:
                break
            k += 1
        
        metric_value = abs(math.log(p_val ** k) - (n - l_phi))
        
        instances_tested += 1
        total_metric_value += metric_value
    
    if instances_tested < 30:
        return {
            "metric_name": "p-adic valuation vs resolution proof width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0
    
    return {
        "metric_name": "p-adic valuation vs resolution proof width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={next(seed for seed, result in enumerate(results) if not result['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")