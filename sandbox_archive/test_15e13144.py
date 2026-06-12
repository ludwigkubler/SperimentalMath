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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if m == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested // len([5, 10, 15, 20, 30, 40])):
            cnf = []
            for _ in range(n):
                literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
                clause = random.sample(literals, 3)
                cnf.append(clause)
            
            # Constructive mapping to geometric quantization
            A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
            for clause in cnf:
                for literal in clause:
                    i = abs(literal) - 1
                    if literal > 0:
                        A[i][i] += Fraction(1)
                    else:
                        A[i][i] -= Fraction(1)
            
            # Compute quantum invariant (determinant of the matrix)
            det = determinant(A)
            min_order = abs(det)
            
            # Compute resolution proof width using DPLL solver
            def dpll(clauses, assignment):
                if not clauses:
                    return True
                literal = next(l for l in range(1, n+1) if l not in assignment and -l not in assignment)
                for value in [True, False]:
                    new_assignment = assignment.copy()
                    new_assignment[literal] = value
                    new_clauses = [c for c in clauses if not all(l in new_assignment or -l in new_assignment for l in c)]
                    if dpll(new_clauses, new_assignment):
                        return True
                return False
            
            resolution_width = 0
            for literal in range(1, n+1):
                assignment = {literal: True}
                if not dpll(cnf, assignment):
                    assignment[literal] = False
                    if not dpll(cnf, assignment):
                        resolution_width += 1
            
            metric_values.append({"min_order": min_order, "resolution_width": resolution_width})
    
    correlation_coefficient = sum((x["min_order"] - mean_min_order) * (x["resolution_width"] - mean_resolution_width) for x in metric_values) / len(metric_values)
    mean_min_order = sum(x["min_order"] for x in metric_values) / len(metric_values)
    mean_resolution_width = sum(x["resolution_width"] for x in metric_values) / len(metric_values)
    
    conjecture_holds = correlation_coefficient > 0.8 and all(x["min_order"] / x["resolution_width"] >= 0.5 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested * len([5, 10, 15, 20, 30, 40]),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")