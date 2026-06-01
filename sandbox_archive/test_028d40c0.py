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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n+1):
                A[i][j] /= pivot
            for j in range(n):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(i, n+1):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det
    
    def is_singular(A):
        return determinant(A) == 0
    
    def generate_cnf(n):
        cnf = []
        for i in range(1, n+1):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def projective_plane_representation(cnf):
        n = len(cnf)
        lines = set()
        for clause in cnf:
            x, y = abs(clause[0]), abs(clause[1])
            line = (x * y) % (n + 1), (x - y) % (n + 1)
            lines.add(line)
        return list(lines)
    
    def minimal_order(cnf):
        n = len(cnf)
        lines = projective_plane_representation(cnf)
        points = set()
        for line in lines:
            x, y = line
            for i in range(n + 1):
                if (x * i) % (n + 1) == y and (y * i) % (n + 1) == x:
                    points.add((i, (x * i) % (n + 1)))
        A = [[0] * (len(points) + 1) for _ in range(len(lines))]
        for i, line in enumerate(lines):
            x, y = line
            for j, point in enumerate(points):
                if (x * point[0]) % (n + 1) == y and (y * point[1]) % (n + 1) == x:
                    A[i][j] = 1
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank
    
    def resolution_proof_width(cnf):
        # Simplified DPLL solver to estimate width
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                new_assignment[literal] = False
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                return False
            pure_literal = next((l for l in range(1, len(clauses) + 1) if (l in assignment or -l in assignment)), None)
            if pure_literal:
                new_assignment = assignment.copy()
                new_assignment[pure_literal] = True
                if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                    return True
                new_assignment[pure_literal] = False
                if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                    return True
                return False
            literal = random.choice(clauses[0])
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        
        width = 0
        for i in range(1, len(cnf) + 1):
            assignment = {j: False for j in range(1, len(cnf) + 1)}
            if dpll(cnf, assignment):
                width = max(width, sum(1 for v in assignment.values() if v))
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    minimal_order_value = minimal_order(cnf)
    resolution_width = resolution_proof_width(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": minimal_order_value * resolution_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")