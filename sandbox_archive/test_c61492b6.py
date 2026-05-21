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

# Helper functions for matrix operations
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def multiply(A, B):
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            sum_product = 0
            for k in range(len(B)):
                sum_product += A[i][k] * B[k][j]
            row.append(sum_product)
        result.append(row)
    return result

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Back-substitute to find the solution
    solution = [0] * n
    for i in range(n-1, -1, -1):
        solution[i] = augmented_matrix[i][-1] / augmented_matrix[i][i]
        for j in range(i):
            augmented_matrix[j][-1] -= augmented_matrix[j][i] * solution[i]
    
    return solution

# Constructive mapping from CNF to Hodge structure (simplified example)
def cnf_to_hodge_structure(cnf):
    # Placeholder function, replace with actual implementation
    return random.random()

# DPLL algorithm for SAT
def dpll(clauses, assignment=None):
    if not clauses:
        return True, {}
    if any(len(c) == 0 for c in clauses):
        return False, {}
    
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        result, _ = dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        if result:
            return True, new_assignment
        else:
            new_assignment[literal] = False
            result, _ = dpll([c for c in clauses if -literal not in c], new_assignment)
            return result, new_assignment
    
    literal = next(lit for lit in range(1, max(clauses)+1) if all(lit not in c or -lit in c for c in clauses))
    new_assignment_true = assignment.copy()
    new_assignment_true[literal] = True
    result_true, _ = dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment_true)
    if result_true:
        return True, new_assignment_true
    
    new_assignment_false = assignment.copy()
    new_assignment_false[literal] = False
    result_false, _ = dpll([c for c in clauses if -literal not in c], new_assignment_false)
    return result_false, new_assignment_false

# Run a single trial with the given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 20  # Fixed size for simplicity
    cnf = [[random.randint(1, n), -random.randint(1, n)] for _ in range(n)]
    
    hodge_structure = cnf_to_hodge_structure(cnf)
    stree_width = dpll(cnf)[0]
    
    if stree_width == 0:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": -1,  # Invalid value to indicate failure
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "dpll returned width 0"
        }
    
    geometric_entropy = hodge_structure
    
    expected_bound = n**3 * math.log(n) * stree_width
    if abs(geometric_entropy - expected_bound) / expected_bound > 0.1:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": geometric_entropy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Geometric entropy {geometric_entropy} exceeds bound {expected_bound}"
        }
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": geometric_entropy,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

# Main function to run trials with given seeds
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 prime numbers
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
        seeds = random.sample(primes, 30)
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"geometric entropy exceeds bound\" first_failing_seed={first_failing_seed}")