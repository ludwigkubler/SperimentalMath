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

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    
    # Forward elimination
    for i in range(n):
        if A_b[i][i] == 0:
            for j in range(i+1, n):
                if A_b[j][i] != 0:
                    A_b[i], A_b[j] = A_b[j], A_b[i]
                    break
            else:
                raise ValueError("No non-zero pivot found")
        
        for j in range(i+1, n):
            factor = A_b[j][i] / A_b[i][i]
            for k in range(n+1):
                A_b[j][k] -= factor * A_b[i][k]
    
    # Backward substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i+1, n))) / A_b[i][i]
    
    return x

def dpll_solver(clauses, assignment):
    if not clauses:
        return True
    if any(all(not clause[i] for i in clause) for clause in clauses):
        return False
    
    literals = set()
    for clause in clauses:
        for literal in clause:
            literals.add(abs(literal))
    
    for literal in literals:
        new_assignment = assignment[:]
        new_assignment[literal-1] = True
        if dpll_solver(clause_substitution(clauses, literal), new_assignment):
            return True
        
        new_assignment[literal-1] = False
        if dpll_solver(clause_substitution(clauses, -literal), new_assignment):
            return True
    
    return False

def clause_substitution(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        elif -literal in clause:
            new_clause = [l for l in clause if l != -literal]
            if new_clause:
                new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    
    return new_clauses

def generate_tseitin_formula(n):
    variables = list(range(1, n+1))
    clauses = []
    
    for i in range(1, n+1):
        clauses.append([i])
        clauses.append([-i])
    
    for i in range(2, n+1):
        for j in range(i-1):
            clauses.append([i, -j])
            clauses.append([-i, j])
    
    return variables, clauses

def local_induction_degree(clauses):
    # Placeholder function to compute the local induction degree
    # This is a dummy implementation and should be replaced with an actual algorithm
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        total_width = 0
        total_lind = 0
        instances_tested = 0
        
        for _ in range(30):
            variables, clauses = generate_tseitin_formula(n)
            assignment = [False] * len(variables)
            
            try:
                width = len(dpll_solver(clauses, assignment))
                lind = local_induction_degree(clauses)
                
                total_width += width
                total_lind += lind
                instances_tested += 1
            except Exception as e:
                return {
                    "metric_name": "lind_over_w",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
        
        if instances_tested < 30:
            return {
                "metric_name": "lind_over_w",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        lind_over_w = total_lind / total_width
        results.append(lind_over_w)
    
    mean_value = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 1.0) / len(results)
    
    return {
        "metric_name": "lind_over_w",
        "metric_value": mean_value,
        "instances_tested": 30 * len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(r > 0 for r in results)),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='lind_over_w > 1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")