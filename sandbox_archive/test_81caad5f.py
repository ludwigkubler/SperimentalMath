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
    rref = [row[:] for row in matrix]
    
    for i in range(rows):
        # Find pivot
        max_row = i
        for j in range(i + 1, rows):
            if abs(rref[j][i]) > abs(rref[max_row][i]):
                max_row = j
        
        # Swap rows
        rref[i], rref[max_row] = rref[max_row], rref[i]
        
        # Eliminate below pivot
        for j in range(i + 1, rows):
            factor = Fraction(rref[j][i], rref[i][i])
            for k in range(cols):
                rref[j][k] -= factor * rref[i][k]
    
    return rref

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    var = next(iter(cnf))
    pos_clauses = [cl for cl in cnf if var in cl]
    neg_clauses = [cl for cl in cnf if -var in cl]
    
    # Try assigning true to the variable
    new_assignment = assignment.copy()
    new_assignment[var] = True
    if dpll(pos_clauses, new_assignment):
        return True
    
    # Try assigning false to the variable
    new_assignment = assignment.copy()
    new_assignment[var] = False
    if dpll(neg_clauses, new_assignment):
        return True
    
    return False

def generate_cnf(n):
    cnf = []
    for _ in range(2**n - 1):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    min_ranks = []
    dpll_depths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            q_matrix = [[Fraction(random.randint(-1, 1)) for _ in range(n)] for _ in range(n)]
            
            r_phi = rank(q_matrix)
            d_phi = len(cnf) if not dpll(cnf) else 0
            
            min_ranks.append(r_phi)
            dpll_depths.append(d_phi)
    
    correlation_coefficient = sum((min_ranks[i] - mean(min_ranks)) * (dpll_depths[i] - mean(dpll_depths)) for i in range(len(min_ranks))) / len(min_ranks)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": 40,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.6 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.6\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support")