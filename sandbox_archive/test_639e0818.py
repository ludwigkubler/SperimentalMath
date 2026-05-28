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
    
    def build_graph(clauses):
        graph = {}
        for clause in clauses:
            for var in clause:
                if var not in graph:
                    graph[var] = set()
                for other_var in clause:
                    if other_var != var and other_var not in graph[var]:
                        graph[var].add(other_var)
                        if other_var not in graph:
                            graph[other_var] = {var}
        return graph
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            # Find the pivot
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below the pivot
            for j in range(i + 1, rows):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(i, cols):
                    matrix[j][k] += factor * matrix[i][k]
        
        # Back-substitute to get the solution
        solution = [0] * cols
        for i in range(rows - 1, -1, -1):
            solution[i] = (matrix[i][-1] - sum(matrix[i][j] * solution[j] for j in range(i + 1, cols))) / matrix[i][i]
        return solution
    
    def min_rank(graph):
        n = len(graph)
        matrix = [[0] * (n + 1) for _ in range(n)]
        for i, neighbors in enumerate(graph.values()):
            for neighbor in neighbors:
                matrix[i][neighbor] = 1
            matrix[i][-1] = 1
        
        return len(gaussian_elimination(matrix))
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        
        # Each variable is true
        for var in variables:
            clauses.append([var])
        
        # At least one variable is false
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([f'~{variables[i]}', f'~{variables[j]}'])
        
        # Each pair of variables must be different
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    clauses.append([f'{variables[i]}', f'{variables[j]}', f'~{variables[k]}'])
        
        return clauses
    
    def resolution_prove(clauses):
        literals = set()
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [l for l in clause1 + clause2 if l not in set(clause1) & set(clause2)]
                        if not any(new_clause == c for c in literals):
                            new_clauses.append(new_clause)
            literals.update(new_clauses)
            clauses.extend(new_clauses)
            if not new_clauses:
                break
        return len(literals)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = tseitin_formula(n)
    graph = build_graph(clauses)
    ν_G = min_rank(graph)
    L_F = resolution_prove(clauses)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": L_F,
        "instances_tested": 1,
        "conjecture_holds": L_F >= 2 ** (math.log(ν_G, 2) * math.log(ν_G, 2)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*100 + 2, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")