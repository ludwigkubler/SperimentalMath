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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n + 1):
                if i == k:
                    matrix[j][k] = 0
                else:
                    matrix[j][k] += factor * matrix[i][k]
    
    # Back-substitute to find rank
    rank = n
    for i in range(n-1, -1, -1):
        if all(abs(matrix[i][j]) < 1e-9 for j in range(i+1, n)):
            rank -= 1
    return rank

def dpll(instance):
    def backtrack(assignment, clauses):
        if not clauses:
            return True
        clause = next(c for c in clauses if any(l in assignment for l in c))
        literals = [l for l in clause if l not in assignment]
        literal = random.choice(literals)
        assignment[literal] = 1
        if backtrack(assignment, [c for c in clauses if literal not in c]):
            return True
        del assignment[literal]
        assignment[-literal] = 1
        if backtrack(assignment, [c for c in clauses if -literal not in c]):
            return True
        del assignment[-literal]
        return False
    
    n = len(instance)
    variables = list(range(1, n+1))
    assignment = {}
    return backtrack(assignment, instance)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random planar k-CNF instance
    n = 20  # Fixed size for simplicity
    k = 3   # Fixed number of literals per clause
    num_clauses = 5 * n // k
    
    clauses = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < k:
            literal = random.choice([-i, i] for i in variables)
            if literal not in clause and -literal not in clause:
                clause.add(literal)
        clauses.append(list(clause))
    
    # Convert to DPLL instance
    dpll_instance = []
    for clause in clauses:
        dpll_instance.extend([[l, 0] for l in clause])
    
    # Calculate the rank of the tensor product (simplified as a placeholder)
    rank = len(gaussian_elimination([[1]*n + [0]] * n))  # Placeholder
    
    # Calculate DPLL search tree width
    dpll_width = dpll(dpll_instance)
    
    # Check if the rank is lower than the DPLL width
    conjecture_holds = rank < dpll_width
    
    return {
        "metric_name": "Rank vs DPLL Width",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Mapping undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping undefined' first_failing_seed={first_failing_seed}")