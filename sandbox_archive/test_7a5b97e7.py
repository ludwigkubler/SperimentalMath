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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def rank_of_matrix(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    
    rank = n
    for row in augmented_matrix:
        if all(x == 0 for x in row[:n]):
            rank -= 1
    
    return rank

def min_representation_rank(matrix):
    n = len(matrix)
    identity = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    
    # Add identity matrix to the right
    augmented_matrix = [row[:] + col[:] for row, col in zip(matrix, identity)]
    
    gaussian_elimination(augmented_matrix)
    
    rank = n
    for row in augmented_matrix:
        if all(x == 0 for x in row[:n]):
            rank -= 1
    
    return rank

def dpll_solver(cnf):
    def solve(assignment, clauses):
        if not clauses:
            return True
        clause = next(clause for clause in clauses if any(lit in assignment and assignment[lit] == 1 for lit in clause))
        pos_lit = next((lit for lit in clause if lit > 0), None)
        neg_lit = next((lit for lit in clause if lit < 0), None)
        
        if pos_lit is not None:
            new_assignment = {**assignment, pos_lit: 1}
            new_clauses = [c for c in clauses if not any(lit in c and assignment[lit] == 1 for lit in c)]
            if solve(new_assignment, new_clauses):
                return True
        if neg_lit is not None:
            new_assignment = {**assignment, neg_lit: -1}
            new_clauses = [c for c in clauses if not any(lit in c and assignment[lit] == 1 for lit in c)]
            if solve(new_assignment, new_clauses):
                return True
        
        return False
    
    variables = set(abs(lit) for clause in cnf for lit in clause)
    assignment = {var: None for var in variables}
    return solve(assignment, cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        matrix_representation = [[random.choice([Fraction(0, 1), Fraction(1, 1)]) for _ in range(n)] for _ in range(n)]
        min_rank = rank_of_matrix(matrix_representation)
        
        cnf_instance = [[random.randint(-n, n) for _ in range(random.randint(2, n//2))] for _ in range(n)]
        dpll_length = len(dpll_solver(cnf_instance))
        
        results.append({
            "n": n,
            "min_rank": min_rank,
            "dpll_length": dpll_length
        })
    
    if not results:
        return {
            "metric_name": "Minimal Representation Rank vs DPLL Proof Length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    
    mean_diff = sum(abs(result["min_rank"] - result["dpll_length"]) for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["min_rank"] - result["dpll_length"]) <= 3) / len(results)
    
    return {
        "metric_name": "Minimal Representation Rank vs DPLL Proof Length",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Mean diff > 3 for {support_fraction*100:.2f}% of trials"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed) for seed in seeds if "metric_value" in run_trial(seed)]
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) <= 3) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=NA support_fraction={support_fraction}")
    elif any(abs(result["metric_value"]) > 3 for result in results):
        first_failing_seed = next(seed for seed in seeds if "metric_value" in run_trial(seed) and abs(run_trial(seed)["metric_value"]) > 3)
        print(f"RESULT: FALSIFIED counterexample='Mean diff > 3' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")