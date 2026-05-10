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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment):
    if not cnf:
        return True
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    for clause in unit_clauses:
        if abs(clause) in assignment and assignment[abs(clause)] != (clause > 0):
            return False
        assignment[abs(clause)] = clause > 0
    literals = [c[0] for c in cnf if len(c) > 1]
    literal, polarity = random.choice(literals), True
    assignment[literal] = polarity
    if dpll(cnf, assignment):
        return True
    del assignment[literal]
    assignment[literal] = not polarity
    return dpll(cnf, assignment)

def count_clauses_satisfied(cnf, assignment):
    satisfied = 0
    for clause in cnf:
        if any(assignment[abs(lit)] == (lit > 0) for lit in clause):
            satisfied += 1
    return satisfied

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    
    assignment = {}
    if dpll(cnf, assignment):
        circuit_size = count_clauses_satisfied(cnf, assignment)
    else:
        circuit_size = float('inf')
    
    adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for lit1 in clause:
            for lit2 in clause:
                if lit1 != lit2:
                    adjacency_matrix[abs(lit1)][abs(lit2)] += 1
    
    eigenvalues = []
    for i in range(1, n + 1):
        v = [1] * (n + 1)
        v[i] = 0
        Av = [sum(adjacency_matrix[i][j] * v[j] for j in range(n + 1)) for j in range(n + 1)]
        eigenvalue = sum(Av[j] * v[j] for j in range(n + 1))
        eigenvalues.append(eigenvalue)
    
    smallest_eigenvalue = min(abs(ev) for ev in eigenvalues if ev != 0)
    
    metric_value = circuit_size / smallest_eigenvalue
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "circuit_size_over_smallest_eigenvalue",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")