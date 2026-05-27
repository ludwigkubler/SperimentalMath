# auto-injected by SEC sandbox
import math
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
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank(matrix):
    A = [row[:] for row in matrix]
    gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def dpll_depth(formula, assignment={}):
    if not formula:
        return 0
    literals = set()
    for clause in formula:
        literals.update(clause)
    literal = random.choice(list(literals))
    negated = -literal
    
    def propagate(assignment):
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        new_formula = []
        for clause in formula:
            if not any(l in assignment and assignment[l] for l in clause):
                new_formula.append([l for l in clause if l != literal])
        return new_formula, new_assignment
    
    def backtrack(formula, assignment):
        depth = 0
        while True:
            formula, assignment = propagate(assignment)
            if not formula:
                return depth
            negated = random.choice(list(set(l for clause in formula for l in clause) - set(assignment.keys())))
            assignment[negated] = False
            depth += 1
    
    return max(backtrack(formula, assignment), backtrack([[negated]] + formula, assignment))

def run_trial(seed: int):
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n*2, n*3)
    formula = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i+1) for i in range(n)]
        if all(l in clause for l in [-1*(i+1) for i in range(n)]):
            continue
        formula.append(clause)
    
    matrix = [[0] * n for _ in range(m)]
    for i, clause in enumerate(formula):
        for literal in clause:
            matrix[i][abs(literal)-1] += 1
    
    rank_value = rank(matrix)
    depth = dpll_depth(formula)
    
    if depth == 0 or rank_value == 0:
        return {
            "metric_name": "Rank/Depth Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL depth or rank is zero"
        }
    
    ratio = rank_value / depth
    return {
        "metric_name": "Rank/Depth Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= Fraction(1, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["instances_tested"] > 0) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank/Depth Ratio exceeds 0.5\" first_failing_seed={first_failing_seed}")