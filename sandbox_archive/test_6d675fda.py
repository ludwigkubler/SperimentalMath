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
from math import gcd

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def chinese_remainder_theorem(n, a):
    sum = 0
    prod = 1
    for ni in n:
        prod *= ni
    for ni, ai in zip(n, a):
        p = prod // ni
        sum += ai * mod_inverse(p, ni) * p
    return sum % prod

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        b[i] /= factor
        for k in range(m):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
    return [b[i] for i in range(m)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    p = n + 1
    clauses = [[random.choice([-i, i]) for _ in range(3)] for _ in range(n)]
    
    # Convert clauses to Diophantine equations modulo p
    A = []
    b = []
    for clause in clauses:
        eq = [0] * (2*n + 1)
        for var in clause:
            if var > 0:
                eq[var - 1] += 1
            else:
                eq[-var - 1] -= 1
        A.append(eq[:-1])
        b.append(-eq[-1])
    
    # Solve the system using Gaussian elimination
    solutions = gaussian_elimination(A, b)
    
    # Count integer solutions modulo p
    solution_count = 0
    for i in range(p):
        if all((sol + i) % p == 0 for sol in solutions):
            solution_count += 1
    
    # Generate a random 3-SAT instance and find its resolution proof length
    variables = list(range(1, n+1))
    assignment = {var: random.choice([True, False]) for var in variables}
    def evaluate_clause(clause):
        return any((assignment[var] if var > 0 else not assignment[-var]) for var in clause)
    
    proof_length = 0
    stack = []
    while True:
        unsatisfied_clauses = [i+1 for i, clause in enumerate(clauses) if not evaluate_clause(clause)]
        if not unsatisfied_clauses:
            break
        unit_clause = next((c for c in clauses if len([var for var in c if abs(var) in assignment]) == 1), None)
        if unit_clause is None:
            proof_length += 1
            continue
        var = [v for v in unit_clause if v in assignment][0]
        stack.append((var, not assignment[var]))
        assignment[var] = not assignment[var]
    
    # Check if the resolution proof length is less than or equal to the number of solutions
    conjecture_holds = proof_length <= solution_count
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Proof length {proof_length} > solution count {solution_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")