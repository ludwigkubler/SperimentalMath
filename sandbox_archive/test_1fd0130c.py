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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def rank(matrix):
    n = len(matrix)
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def generate_cnf(n, m):
    cnf = []
    literals = list(range(1, n+1)) + [-i for i in range(1, n+1)]
    random.shuffle(literals)
    
    for _ in range(m):
        clause = [random.choice(literals) for _ in range(2)]
        cnf.append(clause)
    
    return cnf

def dpll_solver(cnf):
    def solve(model):
        if not cnf:
            return model
        literal = next((lit for lit in literals if lit not in model and -lit not in model), None)
        if literal is None:
            return None
        
        new_model = model + [literal]
        if all(any(lit not in clause or -lit in clause for lit in clause) for clause in cnf):
            result = solve(new_model)
            if result is not None:
                return result
        new_model = model + [-literal]
        if all(any(lit not in clause or -lit in clause for lit in clause) for clause in cnf):
            result = solve(new_model)
            if result is not None:
                return result
        
        return None
    
    literals = list(range(1, len(cnf)+1)) + [-i for i in range(1, len(cnf)+1)]
    return solve([])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    m = 2 * n
    
    cnf = generate_cnf(n, m)
    circuit_size = len(dpll_solver(cnf))
    
    if circuit_size == 0:
        return {
            "metric_name": "R(φ)/s(φ)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "circuit_size_zero"
        }
    
    representation = [[random.choice([-i, i]) for _ in range(n)] for _ in range(n)]
    minimal_rank = rank(representation)
    
    ratio = abs(minimal_rank / circuit_size - 1)
    
    return {
        "metric_name": "R(φ)/s(φ)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 0.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={mean_ratio:.2f} std=NA support_fraction={support_fraction:.2f}")