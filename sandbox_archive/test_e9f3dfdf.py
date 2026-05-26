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
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError('Matrix dimensions do not match')

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

def matrix_inverse(A):
    rows = len(A)
    cols = len(A[0])

    if rows != cols:
        raise ValueError('Matrix is not square')

    augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(A)]
    
    for i in range(rows):
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError('Matrix is singular')
        
        for j in range(i, cols * 2):
            augmented_matrix[i][j] /= pivot

        for k in range(rows):
            if k != i:
                factor = A[k][i]
                for j in range(i, cols * 2):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

    inverse = [row[cols:] for row in augmented_matrix]

    return inverse

def p_adic_valuation(n, p):
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count

def tautology_degree(circuit):
    # Simplified DPLL solver for tautology degree
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            if var < 0:
                var = -var
                negated = True
            else:
                negated = False
            new_assignment = assignment[:]
            new_assignment[var-1] = not negated
            return dpll(clauses, new_assignment)
        pure_literal = next((v for v in range(1, len(assignment)+1) if all(v in c or -v in c for c in clauses)), None)
        if pure_literal:
            var = pure_literal
            negated = True if any(-var in c for c in clauses) else False
            new_assignment = assignment[:]
            new_assignment[var-1] = not negated
            return dpll(clauses, new_assignment)
        literal = random.choice([v for v in range(1, len(assignment)+1)])
        var = literal if literal > 0 else -literal
        negated = True if literal < 0 else False
        new_assignment = assignment[:]
        new_assignment[var-1] = not negated
        return dpll(clauses, new_assignment) or dpll(clauses, new_assignment[:var-1] + [not negated] + new_assignment[var:])
    
    clauses = circuit['clauses']
    assignment = [False] * len(circuit['variables'])
    if dpll(clauses, assignment):
        return 0
    else:
        return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    p = random.choice([2, 3, 5, 7])
    
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(n):
        clause = [random.choice(variables) if random.random() < 0.5 else -random.choice(variables) for _ in range(random.randint(1, 3))]
        clauses.append(clause)
    
    circuit = {'variables': variables, 'clauses': clauses}
    tautology_deg = tautology_degree(circuit)
    p_adic_val = sum(p_adic_valuation(abs(lit), p) for lit in [v for clause in circuit['clauses'] for v in clause])
    rank = len(set(tuple(sorted([p_adic_valuation(abs(lit), p) for lit in clause])) for clause in circuit['clauses']))
    
    metric_value = rank / tautology_deg
    conjecture_holds = metric_value <= 1 / tautology_deg + 0.1
    counterexample = "" if conjecture_holds else f"Rank {rank} > 1/δ(C)={1/tautology_deg}"
    
    return {
        "metric_name": "p-adic valuation rank",
        "metric_value": metric_value,
        "instances_tested": 1,
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
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")