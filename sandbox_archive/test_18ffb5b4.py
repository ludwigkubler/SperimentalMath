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
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0, 1)
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def inverse(A):
    n = len(A)
    I = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    A_augmented = [row + col for row, col in zip(A, I)]
    A_echelon = gaussian_elimination(A_augmented)
    n = len(A_echelon)
    if any(abs(A_echelon[i][i]) < 1e-9 for i in range(n)):
        raise ValueError("Singular matrix")
    A_inv = [[A_echelon[i][n+j] for j in range(n)] for i in range(n)]
    return A_inv

def projective_plane_representation(cnf):
    n = len(cnf)
    lines = []
    for clause in cnf:
        line = set()
        for literal in clause:
            if literal > 0:
                line.add((literal, 1))
            else:
                line.add((-literal, -1))
        lines.append(line)
    return lines

def minimal_order(cnf):
    n = len(cnf)
    lines = projective_plane_representation(cnf)
    A = [[0] * (n+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(i+1, n):
            if any((x, y) in lines[i] and (-x, -y) in lines[j] for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]):
                A[i][j] = A[j][i] = 1
    A[n][n] = 1
    try:
        inv_A = inverse(A)
        minimal_order_value = sum(inv_A[i][i] for i in range(n))
        return minimal_order_value
    except ValueError:
        return float('inf')

def resolution_proof_width(cnf):
    # Simplified DPLL solver to estimate width
    def dpll(clauses, assignment):
        if not clauses:
            return 1
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(new_clauses, new_assignment) + 1
        pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(new_clauses, new_assignment) + 1
        literal = next((l for l in range(1, n+1) if l not in assignment), None)
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        new_clauses_true = [c for c in clauses if literal not in c and -literal not in c]
        width_true = dpll(new_clauses_true, new_assignment_true) + 1
        new_assignment_false = assignment.copy()
        new_assignment_false[-literal] = True
        new_clauses_false = [c for c in clauses if -literal not in c and literal not in c]
        width_false = dpll(new_clauses_false, new_assignment_false) + 1
        return max(width_true, width_false)
    cnf = [[-l if l < 0 else l for l in clause] for clause in cnf]
    assignment = {}
    return dpll(cnf, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = [[random.randint(1, n) for _ in range(random.randint(2, n))] for _ in range(n)]
    minimal_order_value = minimal_order(cnf)
    resolution_width = resolution_proof_width(cnf)
    return {
        "metric_name": "minimal_order",
        "metric_value": minimal_order_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": minimal_order_value <= resolution_width * 2 and minimal_order_value >= resolution_width / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")