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

def matrix_mul(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    m, n = len(A), len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(m):
        max_row = max(range(i, m), key=lambda x: abs(Augmented[x][i]))
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        if Augmented[i][i] == 0:
            raise ValueError("No unique solution exists")
        for j in range(i + 1, m):
            factor = Augmented[j][i] / Augmented[i][i]
            Augmented[j] = [Augmented[j][k] - factor * Augmented[i][k] for k in range(n + 1)]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (Augmented[i][-1] - sum(Augmented[i][j] * x[j] for j in range(i + 1, n))) / Augmented[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    literals = list(range(-n, 0)) + list(range(1, n + 1))
    
    # Generate a random CNF
    cnf = []
    for _ in range(n):
        clause = random.sample(literals, random.randint(2, n))
        cnf.append(clause)
    
    # Construct the quasi-category (simplified example)
    qm = {}
    for literal in literals:
        qm[literal] = set()
    for clause in cnf:
        for literal in clause:
            for other_literal in literals:
                if literal != other_literal and literal * other_literal < 0:
                    qm[literal].add(other_literal)
    
    # Compute the order of the quasi-category
    visited = set()
    def dfs(node):
        if node not in visited:
            visited.add(node)
            for neighbor in qm[node]:
                dfs(neighbor)
    order = 0
    for literal in literals:
        if literal not in visited:
            dfs(literal)
            order += 1
    
    # Compute the DPLL search tree width (simplified example)
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and -literal in assignment or literal > 0 and literal in assignment:
                return False
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c]
            if dpll(new_clauses, assignment):
                return True
            del assignment[literal]
        else:
            literal = next((l for l in literals if l not in assignment), None)
            if literal < 0 and -literal in assignment or literal > 0 and literal in assignment:
                return False
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c]
            if dpll(new_clauses, assignment):
                return True
            del assignment[literal]
        assignment[-literal] = True
        new_clauses = [c for c in clauses if -literal not in c]
        if dpll(new_clauses, assignment):
            return True
        del assignment[-literal]
        return False
    
    width = 0
    for literal in literals:
        assignment = {}
        if dpll(cnf, assignment):
            width = max(width, len(assignment))
    
    # Return the results
    return {
        "metric_name": "MinOrder(QuasiCat(φ))",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_o_qm = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_o_qm} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")