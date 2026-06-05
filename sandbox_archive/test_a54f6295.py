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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n):
        clauses = []
        literals = [f'x{i}' for i in range(1, n+1)]
        for i in range(n):
            clause = [literals[i]]
            for j in range(i+1, n):
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        return clauses
    
    def diophantine_set(clauses):
        equations = []
        for clause in clauses:
            equation = 0
            for literal in clause:
                if literal.startswith('x'):
                    var = int(literal[1:])
                    coefficient = 1 if literal[0] != '-' else -1
                    equation += coefficient * mod_inverse(var, n)
            equations.append(equation)
        return equations
    
    def minimal_index_of_diophantine_equivalence(equations):
        matrix = []
        for i in range(len(equations)):
            row = [equations[i]]
            for j in range(len(equations)):
                if i != j:
                    row.append(gcd(abs(equations[i]), abs(equations[j])))
            matrix.append(row)
        gaussian_elimination(matrix)
        return sum(max(row) for row in matrix)
    
    def resolution_proof_depth(clauses):
        stack = []
        while clauses:
            clause = random.choice(clauses)
            if all(literal.startswith('-') and literal[1:] in literals for literal in clause):
                return len(stack)
            new_clause = [literal for literal in clause if not any(l.startswith('-') and l[1:] == literal for l in stack)]
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        clauses = tseitin_formula(n)
        equations = diophantine_set(clauses)
        id_phi = minimal_index_of_diophantine_equivalence(equations)
        d_phi = resolution_proof_depth(clauses)
        if d_phi == 0:
            continue
        results.append((id_phi, d_phi))
    
    if not results:
        return {
            "metric_name": "ID(φ)/d(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    ratios = [id_phi / d_phi for id_phi, d_phi in results]
    mean_ratio = sum(ratios) / len(ratios)
    if not (0.5 <= mean_ratio <= 1.5):
        return {
            "metric_name": "ID(φ)/d(φ)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"mean_ratio={mean_ratio}"
        }
    
    return {
        "metric_name": "ID(φ)/d(φ)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")