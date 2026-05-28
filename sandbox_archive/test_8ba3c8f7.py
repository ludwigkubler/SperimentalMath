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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
            clauses.append(['~', var])
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append([f'x{i}', f'x{j}', '~', f'x{random.randint(1, n)}'])
                clauses.append(['~', f'x{i}', f'x{j}', '~', f'x{random.randint(1, n)}'])
        return variables, clauses
    
    def build_graph(clauses):
        graph = {}
        for clause in clauses:
            for var in clause[1:]:
                if var not in graph:
                    graph[var] = set()
                for other_var in clause[1:]:
                    if other_var != var and other_var not in graph[var]:
                        graph[var].add(other_var)
                        graph[other_var].add(var)
        return graph
    
    def min_rank(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, node in enumerate(sorted(graph)):
            for neighbor in graph[node]:
                j = sorted(graph).index(neighbor)
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                pivot_row = -1
                for j in range(rank, rows):
                    if matrix[j][i]:
                        pivot_row = j
                        break
                if pivot_row == -1:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(rows):
                    if j != rank and matrix[j][i]:
                        factor = Fraction(matrix[j][i], matrix[rank][i])
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[rank][k]
                rank += 1
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    def resolution_length(clauses, variables):
        stack = []
        while clauses:
            literal = random.choice([c for c in clauses if len(c) == 1])
            if literal[0] == '~':
                literal = literal[1]
                if literal in stack:
                    return float('inf')
                else:
                    stack.append(literal)
            else:
                if literal not in stack:
                    return float('inf')
                else:
                    stack.remove(literal)
        return len(stack) * 2
    
    def spearman_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i for i in range(n)}
        rank_y = {y[i]: i for i in range(n)}
        sum_d1_squared = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_d1_squared) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        graph = build_graph(clauses)
        ν_G = min_rank(graph)
        L_F = resolution_length(clauses, variables)
        results.append((ν_G, L_F))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_trials"
        }
    
    ν_Gs, L_Fs = zip(*results)
    rho = spearman_correlation(ν_Gs, L_Fs)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Spearman correlation < 0.95' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")