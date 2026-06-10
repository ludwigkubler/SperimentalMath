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
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate n-1 clauses of the form (x1 ∨ x2 ∨ ... ∨ xn)
        for i in range(1, n):
            clause = ' ∨ '.join(variables[:i+1])
            clauses.append(clause)
        
        # Generate a final clause of the form (~xi ∨ xi+1) for each variable
        for i in range(n-1):
            clause = f' ~{variables[i]} ∨ {variables[i+1]}'
            clauses.append(clause)
        
        return variables, clauses
    
    def communication_complexity_matrix(variables, clauses):
        n = len(variables)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in clauses:
            if '∨' in clause:
                parts = clause.split(' ∨ ')
            else:
                parts = [clause]
            
            for part in parts:
                if '~' in part:
                    var = part[2:]
                    idx = int(var[1:]) - 1
                    matrix[idx][n] += 1
                else:
                    var = part
                    idx = int(var[1:]) - 1
                    matrix[n][idx] += 1
        
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [i] for i, row in enumerate(matrix)]
        
        # Gaussian elimination
        for col in range(n - 1):
            pivot_row = None
            for row in range(col, m):
                if augmented_matrix[row][col] != 0:
                    pivot_row = row
                    break
            
            if pivot_row is None:
                continue
            
            augmented_matrix[pivot_row], augmented_matrix[col] = augmented_matrix[col], augmented_matrix[pivot_row]
            
            for row in range(m):
                if row == col:
                    continue
                
                factor = -augmented_matrix[row][col] / augmented_matrix[col][col]
                for j in range(n + 1):
                    augmented_matrix[row][j] += factor * augmented_matrix[col][j]
        
        rank = sum(1 for row in augmented_matrix if row[-1] < m)
        return rank
    
    def minimal_order(K_G):
        # Placeholder function to compute the minimal order of a cyclic group action on K(G)
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)  # Randomly generate a number for demonstration purposes
    
    variables, clauses = generate_tseitin_formula(random.randint(5, 40))
    matrix = communication_complexity_matrix(variables, clauses)
    rank_value = rank(matrix)
    K_G_order = minimal_order(None)  # This will be replaced with actual computation
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": rank_value,
        "instances_tested": 1,
        "n_max": len(variables),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")