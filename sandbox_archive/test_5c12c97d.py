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
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def chinese_remainder_theorem(residues, moduli):
    total = 0
    prod = math.prod(moduli)
    for n_i, a_i in zip(moduli, residues):
        p = prod // n_i
        total += a_i * mod_inverse(p, n_i) * p
    return total % prod

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def linear_diophantine_system(n, clauses, p):
    m = len(clauses)
    A = [[0] * n for _ in range(m)]
    b = [0] * m
    for i, clause in enumerate(clauses):
        for literal in clause:
            var_index = abs(literal) - 1
            if literal > 0:
                A[i][var_index] += 1
            else:
                A[i][var_index] -= 1
        b[i] = 1 if any(lit > 0 for lit in clause) else -1
    solutions = []
    for x in range(p):
        if all((A[i][j] * x + b[i]) % p == 0 for i in range(m)):
            solutions.append(x)
    return len(solutions)

def dpll_with_memoization(clauses, assignment, model):
    if not clauses:
        return True
    literal = next(lit for lit in range(1, len(model) + 1) if lit not in model and -lit not in model)
    new_clauses = [c for c in clauses if literal not in c and -literal not in c]
    if dpll_with_memoization(new_clauses, assignment | {literal}, model | {literal}):
        return True
    if dpll_with_memoization(new_clauses, assignment | {-literal}, model | {-literal}):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    p = n + 1
    clauses = [[random.choice([-i, i]) for _ in range(3)] for _ in range(n)]
    diophantine_solutions = linear_diophantine_system(n, clauses, p)
    
    def is_clause_true(clause):
        return any(model[var_index] == literal for var_index, literal in enumerate(clause))
    
    model = {}
    if dpll_with_memoization(clauses, set(), model):
        resolution_length = len(model)
    else:
        resolution_length = float('inf')
    
    metric_name = "Resolution Length"
    metric_value = resolution_length
    instances_tested = 1
    conjecture_holds = resolution_length <= diophantine_solutions
    counterexample = "" if conjecture_holds else f"n={n}, p={p}, clauses={clauses}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
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
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_failing['counterexample']}\" first_failing_seed={first_failing['seed']}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")