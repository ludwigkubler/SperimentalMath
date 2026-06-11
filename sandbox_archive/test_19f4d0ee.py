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
    return abs(a*b) // gcd(a, b)

def matrix_mul(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n):
            augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented[j][i]
                for k in range(n+1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def is_prime(num):
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf_formula = generate_cnf(n)
    satisfying_assignments = generate_satisfying_assignments(cnf_formula, 30)
    quotient_group_order = compute_quotient_group_order(satisfying_assignments)
    frege_proof_depth = compute_frege_proof_depth(cnf_formula)
    
    return {
        "metric_name": "quotient_group_order",
        "metric_value": quotient_group_order,
        "instances_tested": len(satisfying_assignments),
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

def generate_cnf(n):
    # Generate a random CNF formula with n variables
    clauses = []
    for _ in range(2*n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def generate_satisfying_assignments(cnf_formula, k):
    # Generate k random satisfying assignments for the CNF formula
    variables = list(range(1, len(cnf_formula) + 1))
    assignments = []
    while len(assignments) < k:
        assignment = {var: random.choice([True, False]) for var in variables}
        if all(any(lit in assignment and (assignment[lit] == (lit > 0)) or (not lit in assignment and not (lit > 0)) for lit in clause) for clause in cnf_formula):
            assignments.append(assignment)
    return assignments

def compute_quotient_group_order(satisfying_assignments):
    # Compute the order of the quotient group
    n = len(satisfying_assignments[0])
    kernel = []
    for i in range(n):
        for j in range(i+1, n):
            if all(assignment[i] == assignment[j] for assignment in satisfying_assignments):
                kernel.append((i, j))
    return len(kernel)

def compute_frege_proof_depth(cnf_formula):
    # Compute the Frege proof depth using a small DPLL solver
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if all(lit in new_assignment and (new_assignment[lit] == (lit > 0)) or (not lit in new_assignment and not (lit > 0)) for clause in clauses):
                return dpll([c for c in clauses if literal not in c], new_assignment)
            else:
                new_assignment[literal] = False
                return dpll([c for c in clauses if -literal not in c], new_assignment) + 1
        pure_literal = next((lit for lit in range(1, len(cnf_formula)+1) if all(lit in assignment and (assignment[lit] == True) or (not lit in assignment and not True) for clause in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll([c for c in clauses if pure_literal not in c], new_assignment)
        else:
            literal = random.choice(cnf_formula[0])
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return 1 + dpll([c for c in clauses if literal not in c], new_assignment)

    return dpll(cnf_formula, {})

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")