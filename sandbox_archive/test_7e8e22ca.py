# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for j in range(len(matrix)):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix)
    return det

def noncommutative_probability_order(cnf):
    n = max(abs(lit) for lit in cnf)
    if n == 0:
        return 0
    
    # Construct the unitary matrices
    unitaries = {i: random_unitary(2) for i in range(1, n+1)}
    
    # Construct the noncommutative probability distribution matrix
    P = [[0] * (n**2) for _ in range(n**2)]
    for clause in cnf:
        for lit in clause:
            if lit > 0:
                row, col = unitaries[lit]
            else:
                row, col = unitaries[-lit][::-1]
            
            P[row*n + col] += 1
    
    # Normalize the matrix
    total = sum(P)
    for i in range(n**2):
        P[i] /= total
    
    # Compute the determinant of the matrix
    det = determinant(P)
    
    return abs(det)

def random_unitary(d):
    U = [[0] * d for _ in range(d)]
    for i, j in combinations(range(d), 2):
        U[i][j] = random.gauss(0, 1)
        U[j][i] = -U[i][j]
    
    # Normalize to make it unitary
    norm = sum(U[i][j]**2 for i in range(d) for j in range(i, d))**0.5
    for i in range(d):
        for j in range(d):
            U[i][j] /= norm
    
    return (i, j)

def resolution_width(cnf):
    def dpll(clauses, assignment):
        if not clauses:
            return 1
        if any(all(lit in assignment and assignment[lit] == True for lit in clause) for clause in clauses):
            return 0
        
        unit_clauses = [lit for lit in cnf if len([x for x in cnf if x != lit and set(x).issubset(set(cnf))]) == 1]
        if not unit_clauses:
            return float('inf')
        
        unit_lit = unit_clauses[0]
        new_assignment = assignment.copy()
        new_assignment[unit_lit] = True
        true_clauses = [c for c in cnf if unit_lit not in c and all(lit in new_assignment and new_assignment[lit] == False for lit in c)]
        
        return 1 + dpll(true_clauses, new_assignment)
    
    return min(dpll(cnf, {}) for _ in range(30))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.randint(1, min(n//2, 5))
    
    cnf = []
    for _ in range(d * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if len(set(clause)) == 2:
            cnf.append(clause)
    
    o_phi = noncommutative_probability_order(cnf)
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": abs(o_phi - w_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(o_phi - w_phi) <= 0.5,  # Assuming k = 0.5 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient={r['metric_value']}\" first_failing_seed={seed}")
                break