# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def minimal_index_of_kahler_metric(clause_set):
    variables = set()
    for clause in clause_set:
        for literal in clause:
            variables.add(abs(literal))
    
    n = len(variables)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    for clause in clause_set:
        for literal in clause:
            i = variables.index(abs(literal))
            if literal > 0:
                A[i][i] += 1
            else:
                A[i][i] -= 1
    
    x = gaussian_elimination(A, b)
    return max(x)

def find_resolution_refutation(clause_set):
    # Simplified DPLL solver for Tseitin clauses
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and literal in assignment:
                return False
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if not dpll([c for c in clauses if literal not in c], new_assignment):
                new_assignment[literal] = False
                if literal not in assignment:
                    return False
        else:
            literal = next((v for v in variables if v not in assignment), None)
            if not dpll(clauses, assignment | {literal: True}):
                if literal not in assignment:
                    return dpll(clauses, assignment | {literal: False})
        return False
    
    variables = set()
    for clause in clause_set:
        for literal in clause:
            variables.add(abs(literal))
    
    clauses = [[-l if l < 0 else l for l in clause] for clause in clause_set]
    assignment = {}
    if dpll(clauses, assignment):
        return []
    else:
        # Find a refutation
        refutation = []
        for literal in variables:
            if literal not in assignment or not assignment[literal]:
                refutation.append(-literal)
        return refutation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    clause_set = []
    for _ in range(n):
        num_literals = random.randint(2, 5)
        literals = set()
        while len(literals) < num_literals:
            literal = random.choice([-1, 1]) * (random.randint(1, n) + n)
            literals.add(literal)
        clause_set.append(list(literals))
    
    kahler_index = minimal_index_of_kahler_metric(clause_set)
    refutation = find_resolution_refutation(clause_set)
    if not refutation:
        return {
            "metric_name": "kahler_index",
            "metric_value": kahler_index,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_refutation_not_found"
        }
    
    k = len(refutation)
    if kahler_index > 2**k:
        return {
            "metric_name": "kahler_index",
            "metric_value": kahler_index,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"kahler_index={kahler_index} > 2^k={2**k}"
        }
    
    return {
        "metric_name": "kahler_index",
        "metric_value": kahler_index,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [53, 79, 101]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = (sum((x - mean)**2 for x in metric_values) / len(metric_values))**0.5
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if r["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples_found")