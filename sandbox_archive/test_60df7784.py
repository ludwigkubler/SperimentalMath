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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def dpll_with_clause_learning(clauses, variables):
    def backtrack(assignment):
        unassigned = [v for v in variables if v not in assignment]
        if not unassigned:
            if all(all(lit in assignment and (lit > 0) == assignment[lit] for lit in clause) or any(lit in assignment and (lit < 0) == assignment[lit] for lit in clause) for clause in clauses):
                return True
            else:
                return False
        v = unassigned[0]
        assignment[v] = True
        if backtrack(assignment):
            return True
        assignment[v] = False
        assignment[-v] = True
        if backtrack(assignment):
            return True
        del assignment[v]
        del assignment[-v]
        return False
    
    variables = list(range(1, len(clauses) + 1))
    return backtrack({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        if all(lit != -lit for lit in clause):
            clauses.append(clause)
    
    variables = list(range(1, n + 1))
    proof_size = dpll_with_clause_learning(clauses, variables)
    
    if not proof_size:
        return {
            "metric_name": "total_persistence",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_not_found"
        }
    
    A = [[0] * (2 ** n) for _ in range(2 ** n)]
    b = [0] * (2 ** n)
    for i in range(2 ** n):
        bin_i = f"{i:0{n}b}"
        for j in range(n):
            if bin_i[j] == '1':
                A[i][i ^ (1 << j)] += 1
                b[i] += 1
    
    x = gaussian_elimination(A, b)
    total_persistence = sum(abs(x[i]) for i in range(2 ** n))
    
    k = 0.5  # Hypothesis: k ≈ 0.5 based on heuristic reasoning
    expected_persistence = k * math.log(n) / proof_size
    
    return {
        "metric_name": "total_persistence",
        "metric_value": total_persistence,
        "instances_tested": 1,
        "conjecture_holds": abs(total_persistence - expected_persistence) < 0.1 * expected_persistence,
        "counterexample": "" if abs(total_persistence - expected_persistence) < 0.1 * expected_persistence else f"total_persistence={total_persistence}, expected_persistence={expected_persistence}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_persistence_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(total_persistence_values) / len(total_persistence_values)} std={math.sqrt(sum((x - sum(total_persistence_values) / len(total_persistence_values)) ** 2 for x in total_persistence_values) / len(total_persistence_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")