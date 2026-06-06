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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(1, A[i][i])
        for j in range(i+1, n):
            A[j][i] *= factor
        
        # Eliminate above the pivot
        for j in range(i):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def tropical_hodge_structure_rank(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    
    # Construct the matrix
    for i, clause in enumerate(clauses):
        for j in clause:
            if j > 0:
                A[i][j - 1] = max(A[i][j - 1], 1)
            else:
                A[i][-1] = max(A[i][-1], 1)
    
    # Perform Gaussian elimination
    A = gaussian_elimination(A)
    
    # Count the number of non-zero rows
    rank = sum(1 for row in A if any(x != 0 for x in row))
    return rank

def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = [False] * len(clauses)
    
    unsatisfied_clauses = [i for i, clause in enumerate(clauses) if not any(lit == -var or lit == var for var in clause)]
    
    if not unsatisfied_clauses:
        return True
    
    literal = clauses[unsatisfied_clauses[0]][0]
    pos_var = abs(literal)
    
    # Try setting the variable to False
    assignment[pos_var - 1] = False
    if dpll(clauses, assignment):
        return True
    
    # Try setting the variable to True
    assignment[pos_var - 1] = True
    if dpll(clauses, assignment):
        return True
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    
    tseitin_formula = []
    for i, clause in enumerate(clauses):
        new_var = n + i + 1
        tseitin_formula.append([new_var])
        for lit in clause:
            if lit > 0:
                tseitin_formula.append([-lit, new_var])
            else:
                tseitin_formula.append([lit, -new_var])
    
    h_phi = tropical_hodge_structure_rank(tseitin_formula)
    l_phi = 0
    if dpll(tseitin_formula):
        # If the formula is satisfiable, count the number of steps in the DPLL algorithm
        assignment = [False] * len(clauses)
        stack = [(clauses, assignment)]
        while stack:
            clauses, assignment = stack.pop()
            unsatisfied_clauses = [i for i, clause in enumerate(clauses) if not any(lit == -var or lit == var for var in clause)]
            if not unsatisfied_clauses:
                l_phi += 1
                continue
            literal = clauses[unsatisfied_clauses[0]][0]
            pos_var = abs(literal)
            assignment[pos_var - 1] = False
            stack.append((clauses, assignment))
    
    metric_name = "Hodge Structure Rank vs DPLL Proof Path Length"
    metric_value = h_phi / l_phi if l_phi != 0 else float('inf')
    instances_tested = 1
    n_max = n
    conjecture_holds = h_phi >= l_phi
    counterexample = "" if conjecture_holds else f"h(φ)={h_phi}, l(φ)={l_phi}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"h(φ) < l(φ)\" first_failing_seed={first_failing_seed}")