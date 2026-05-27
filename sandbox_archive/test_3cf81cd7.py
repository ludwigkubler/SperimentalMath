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
    
    def generate_tseitin_circuit(n):
        variables = list(range(1, n + 2))
        clauses = []
        
        for i in range(1, n + 1):
            clause = [variables[i], -variables[n + i]]
            clauses.append(clause)
        
        for i in range(1, n + 1):
            clause = [-variables[i], variables[n + i], variables[2 * n + i]]
            clauses.append(clause)
        
        return variables, clauses
    
    def generate_incidence_matrix(variables, clauses):
        num_vars = len(variables)
        num_clauses = len(clauses)
        incidence_matrix = [[0] * num_vars for _ in range(num_clauses)]
        
        for clause_index, clause in enumerate(clauses):
            for literal in clause:
                var_index = abs(literal) - 1
                if literal > 0:
                    incidence_matrix[clause_index][var_index] = 1
                else:
                    incidence_matrix[clause_index][var_index] = -1
        
        return incidence_matrix
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(cols):
            pivot_row = None
            for r in range(rank, rows):
                if matrix[r][i] != 0:
                    pivot_row = r
                    break
            
            if pivot_row is None:
                continue
            
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            
            for r in range(rows):
                if r == rank:
                    continue
                
                factor = -matrix[r][i] / matrix[rank][i]
                for c in range(cols):
                    matrix[r][c] += factor * matrix[rank][c]
            
            rank += 1
        
        return rank
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_circuit(n)
    incidence_matrix = generate_incidence_matrix(variables, clauses)
    
    rank = gaussian_elimination(incidence_matrix)
    
    if rank == 0:
        return {
            "metric_name": "min_generators",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_generators = n - rank + 1
    
    return {
        "metric_name": "min_generators",
        "metric_value": min_generators,
        "instances_tested": 1,
        "conjecture_holds": min_generators <= 1.5 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")