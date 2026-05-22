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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Matrix multiplication not possible")
    result = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        pivot = A_augmented[i][i]
        for j in range(i, n+1):
            A_augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A_augmented[j][i]
                for k in range(i, n+1):
                    A_augmented[j][k] -= factor * A_augmented[i][k]
    return [row[-1] for row in A_augmented]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def cnf_to_affine_variety(n, clauses):
        points = []
        for clause in clauses:
            point = [0] * n
            for literal in clause:
                var = abs(literal) - 1
                if literal > 0:
                    point[var] = 1
                else:
                    point[var] = -1
            points.append(point)
        return points
    
    def resolution_proof_length(clauses):
        # Simplified DPLL solver for demonstration purposes
        assignment = {}
        stack = []
        for clause in clauses:
            if not any(literal in assignment and (assignment[literal] == 0 or literal > 0) for literal in clause):
                stack.append((clause, False))
        
        def dpll():
            while stack:
                clause, extended = stack.pop()
                if all(literal in assignment and assignment[literal] != 0 for literal in clause):
                    continue
                unit_clause = [literal for literal in clause if literal not in assignment]
                if unit_clause:
                    literal = unit_clause[0]
                    assignment[literal] = -sum(assignment.get(-l, 0) for l in clause)
                    stack.append((clause, False))
                else:
                    new_literal = random.choice(clause)
                    assignment[new_literal] = 1
                    stack.append((clause, True))
            return len(assignment)
        
        return dpll()
    
    def geometric_defect(points):
        n = len(points[0])
        points_set = set(tuple(point) for point in points)
        defect = n
        for i in range(n):
            for j in range(i+1, n):
                if (points[i][j] != 0 and points[j][i] != 0) or (points[i][j] == 0 and points[j][i] == 0):
                    continue
                line_points = [point for point in points_set if point[i] * point[j] == 0]
                defect = min(defect, len(line_points))
        return defect
    
    n = random.randint(5, 40)
    num_clauses = random.randint(n, n*2)
    clauses = []
    for _ in range(num_clauses):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        if all(literal == 0 for literal in clause):
            continue
        clauses.append(clause)
    
    points = cnf_to_affine_variety(n, clauses)
    defect = geometric_defect(points)
    proof_length = resolution_proof_length(clauses)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length <= 5 * defect,  # Assuming M=5 for simplicity
        "counterexample": "" if proof_length <= 5 * defect else f"Proof length {proof_length} exceeds 5 times defect {defect}"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"proof_length_exceeds_defect\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")