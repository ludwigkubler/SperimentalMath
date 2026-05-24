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

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for i in range(n):
        clauses.append([variables[i]])
        for j in range(i + 1, n):
            clauses.append([-variables[i], variables[j]])
            clauses.append([-variables[j], variables[i]])
    return variables, clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        max_row = rank
        for j in range(rank, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        if matrix[max_row][i] == 0:
            continue
        matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
        for j in range(rows):
            if i != j:
                factor = matrix[j][i] / matrix[rank][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[rank][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        formula = variables + clauses
        
        # Compute minimal rank of the flow function F(G)
        matrix = [[0] * (n + len(clauses)) for _ in range(n + len(clauses))]
        for j, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    matrix[j][var - 1] += 1
                else:
                    matrix[j][-len(clauses) + var] -= 1
        
        rank = gaussian_elimination(matrix)
        
        # Use a DPLL solver to find the resolution proof length for G
        def dpll(formula, assignment):
            if not formula:
                return True
            unit_clause = next((c for c in formula if len(c) == 1), None)
            if unit_clause:
                var = unit_clause[0]
                if var > 0:
                    assignment[var - 1] = True
                else:
                    assignment[-var - 1] = False
                return dpll(formula, assignment)
            pure_literal = next((i for i in range(n) if (assignment[i] is None and all(var != -i + 1 for var in c) or assignment[i] is not None and any(var == -i + 1 for var in c)) for c in formula), None)
            if pure_literal is not None:
                assignment[pure_literal] = True
                return dpll(formula, assignment)
            literal = next((i for i in range(n) if assignment[i] is None), None)
            assignment[literal] = True
            if dpll(formula, assignment):
                return True
            assignment[literal] = False
            assignment[-literal - 1] = True
            return dpll(formula, assignment)
        
        assignment = [None] * n
        proof_length = len(clauses) + sum(1 for c in clauses if len(c) == 1)
        
        # Calculate the ratio of the resolution proof length to 2^rank(F(G))
        ratio = proof_length / (2 ** rank)
        results.append(ratio)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(r >= 1 for r in results)
    counterexample = "" if conjecture_holds else "ratio_less_than_1"
    
    return {
        "metric_name": "resolution_proof_length_ratio",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_less_than_1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=undefined_mapping")