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
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    
    for r in range(rows):
        if matrix[r][rank] == 0:
            swap_found = False
            for i in range(r + 1, rows):
                if matrix[i][rank] != 0:
                    matrix[r], matrix[i] = matrix[i], matrix[r]
                    swap_found = True
                    break
            if not swap_found:
                continue
        
        pivot = Fraction(matrix[r][rank])
        
        for c in range(cols):
            matrix[r][c] /= pivot
        
        for i in range(rows):
            if i != r and matrix[i][rank] != 0:
                factor = -matrix[i][rank]
                for c in range(cols):
                    matrix[i][c] += factor * matrix[r][c]
        
        rank += 1
        if rank == cols:
            break
    
    return rank

def minimal_rank(boolean_function):
    n = len(boolean_function)
    augmented_matrix = [[0] * (n + 1) for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            augmented_matrix[i][j] = boolean_function[i][j]
        augmented_matrix[i][n] = boolean_function[i][-1]
    
    return gaussian_elimination(augmented_matrix)

def resolution_width(boolean_function):
    n = len(boolean_function)
    clauses = [set(clause) for clause in boolean_function if isinstance(clause, list)]
    variables = set.union(*clauses)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause.pop()
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c - {literal} for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c - {-literal} for c in clauses if -literal not in c], new_assignment):
                return True
        else:
            literal = next(iter(variables))
            if dpll(clauses, assignment | {literal: True}):
                return True
            if dpll(clauses, assignment | {literal: False}):
                return True
        return False
    
    max_width = 0
    for assignment in itertools.product([False, True], repeat=n):
        width = sum(1 for var in variables if assignment[var])
        if not dpll(clauses, assignment):
            max_width = max(max_width, width)
    
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    boolean_function = [[random.choice([True, False]) for _ in range(n)] + [random.choice([True, False])] for _ in range(n)]
    
    rank = minimal_rank(boolean_function)
    width = resolution_width(boolean_function)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= width,
        "counterexample": "" if rank >= width else f"rank={rank}, width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < width\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")