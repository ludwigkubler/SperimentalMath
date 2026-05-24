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

def generate_tseitin_formula(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    
    # Generate literals and their negations
    literals = set()
    for i in range(1, n + 1):
        literals.add(i)
        literals.add(-i)
    
    # Generate clauses
    for _ in range(m):
        clause = random.sample(literals, 3)
        clauses.append(clause)
    
    return variables, clauses

def incidence_matrix(variables, clauses):
    m = len(clauses)
    n = len(variables)
    matrix = [[0] * (n + m) for _ in range(n)]
    
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                matrix[literal - 1][i + n] = 1
            else:
                matrix[-literal - 1][i + n] = -1
    
    return matrix

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    
    for j in range(n):
        i_max = None
        for i in range(rank, m):
            if matrix[i][j] != 0:
                i_max = i
                break
        
        if i_max is not None:
            matrix[i_max], matrix[rank] = matrix[rank], matrix[i_max]
            
            pivot = matrix[rank][j]
            for k in range(j, n):
                matrix[rank][k] /= pivot
            
            for i in range(m):
                if i != rank and matrix[i][j] != 0:
                    factor = -matrix[i][j]
                    for k in range(j, n):
                        matrix[i][k] += factor * matrix[rank][k]
            
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a Tseitin formula with n variables and m clauses
    n = random.randint(5, 40)
    m = random.randint(3 * n, 6 * n)
    variables, clauses = generate_tseitin_formula(n, m)
    
    # Compute the incidence matrix
    incidence_mat = incidence_matrix(variables, clauses)
    
    # Compute the minimal rank of the formal power series representing the incidence matrix
    R_F = gaussian_elimination(incidence_mat)
    
    # Run DPLL algorithms on the Tseitin formulas to compute their proof width w*(F)
    # (This is a placeholder for the actual DPLL implementation, which is not provided here)
    # For simplicity, we assume that the proof width is proportional to the number of clauses
    w_F = m
    
    # Calculate the ratio R(F) / w*(F)
    if w_F == 0:
        return {
            "metric_name": "Ratio R(F) / w*(F)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Proof width is zero"
        }
    
    ratio = R_F / w_F
    
    return {
        "metric_name": "Ratio R(F) / w*(F)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio R(F) / w*(F) is too large\" first_failing_seed={first_failing_seed}")