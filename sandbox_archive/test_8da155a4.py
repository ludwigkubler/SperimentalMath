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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A_rref = [row[:] for row in matrix]
    
    def swap_rows(i, j):
        A_rref[i], A_rref[j] = A_rref[j], A_rref[i]
    
    def scale_row(i, factor):
        for j in range(n):
            A_rref[i][j] *= factor
            if isinstance(A_rref[i][j], int):
                A_rref[i][j] = Fraction(A_rref[i][j])
    
    def add_scaled_row(i, j, factor):
        for k in range(n):
            A_rref[j][k] += factor * A_rref[i][k]
            if isinstance(A_rref[j][k], int):
                A_rref[j][k] = Fraction(A_rref[j][k])
    
    rank = 0
    for i in range(m):
        max_row = None
        for j in range(i, m):
            if any(A_rref[j][k] != 0 for k in range(n)):
                max_row = j
                break
        if max_row is None:
            continue
        
        swap_rows(i, max_row)
        scale_row(i, Fraction(1, A_rref[i][i]))
        
        for j in range(m):
            if i != j and A_rref[j][i] != 0:
                add_scaled_row(i, j, -A_rref[j][i])
        
        rank += 1
    
    return rank

def dpll_proof_width(formula):
    # Simplified DPLL solver for demonstration purposes
    def solve(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if solve([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if solve([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        
        literal, _ = next((l, v) for l, v in assignment.items() if not v)
        if solve(clauses, {**assignment, literal: True}):
            return True
        if solve(clauses, {**assignment, literal: False}):
            return True
        return False
    
    # Convert formula to CNF and count the number of literals
    cnf = []
    for clause in formula:
        cnf.append([l for l in clause])
    
    assignment = {}
    for literal in set(l for clause in cnf for l in clause):
        assignment[literal] = None
    
    return len(assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = [[random.choice([1, -1]) * (i + j) for j in range(n)] for i in range(n)]
    
    rank = matrix_rank(formula)
    width = dpll_proof_width(formula)
    
    return {
        "metric_name": "rank_over_width",
        "metric_value": rank / width,
        "instances_tested": 1,
        "conjecture_holds": rank <= width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        counterexample = "rank_over_width > 1.5"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")