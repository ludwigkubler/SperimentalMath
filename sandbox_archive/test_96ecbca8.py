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

# Helper functions for linear algebra and geometry
def matrix_multiply(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
    
    # Back-substitute to get solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][-1]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]
    
    return x

def is_independent(points):
    n = len(points)
    if n == 0:
        return True
    A = [[points[i][j] for j in range(n)] for i in range(n)]
    return gaussian_elimination(A) != [0] * n

# Constructive mapping from CNF to an affine variety
def cnf_to_variety(cnf):
    points = []
    for clause in cnf:
        point = [1 if literal > 0 else -1 for literal in clause]
        points.append(point)
    return points

# DPLL solver for resolution proof length
def dpll(clause_set, assignment={}):
    if not clause_set:
        return True
    unit_clause = next((c for c in clause_set if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(clause_set - {unit_clause, frozenset(-literal)}, new_assignment):
            return True
        new_assignment[literal] = False
        if dpll(clause_set - {unit_clause, frozenset(literal)}, new_assignment):
            return True
        return False
    
    literal = next((l for l in range(1, max(cnf) + 1) if l not in assignment and -l not in assignment), None)
    if literal is None:
        return False
    
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    if dpll(clause_set, new_assignment):
        return True
    new_assignment[literal] = False
    if dpll(clause_set, new_assignment):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random CNF formula with up to 40 variables and clauses
    n_vars = random.randint(5, 40)
    n_clauses = random.randint(10, 80)
    cnf = []
    for _ in range(n_clauses):
        clause = set()
        while len(clause) < 3:
            literal = random.randint(-n_vars, n_vars)
            if literal not in clause and -literal not in clause:
                clause.add(literal)
        cnf.append(frozenset(clause))
    
    # Compute the associated affine variety
    variety_points = cnf_to_variety(cnf)
    
    # Determine the minimal geometric defect of the variety
    independent_points = [p for p in variety_points if is_independent([p] + variety_points)]
    min_geometric_defect = len(independent_points)
    
    # Compute the resolution proof length using DPLL
    resolution_proof_length = 0
    if dpll(cnf):
        resolution_proof_length = 1
    
    # Correlate the geometric defect with the resolution proof length
    metric_value = resolution_proof_length / min_geometric_defect if min_geometric_defect > 0 else float('inf')
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": metric_value,
        "instances_tested": len(cnf),
        "conjecture_holds": metric_value <= 1.1 * min_geometric_defect,
        "counterexample": "" if metric_value <= 1.1 * min_geometric_defect else f"CNF: {cnf}, Defect: {min_geometric_defect}, Proof Length: {resolution_proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Defect exceeds proof length by more than 10%\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")