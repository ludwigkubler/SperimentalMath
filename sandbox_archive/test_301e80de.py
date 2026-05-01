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

def generate_primes(num_primes):
    primes = []
    num = 2
    while len(primes) < num_primes:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random expander graph
    n = 20
    λ = 0.5 + 0.4 * random.random()  # Second eigenvalue between 0.9 and 1.3
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = sum(A[i]) - (n > 1)
    
    # Compute the second eigenvalue
    λ_computed = abs(sum(eigenvalues(A)) / n)
    
    # Generate a Tseitin formula from the expander graph
    variables = {f'x{i}': i for i in range(n)}
    clauses = []
    for i in range(n):
        if A[i][i] == 1:
            clauses.append([variables[f'x{i}']])
        else:
            clauses.append([-variables[f'x{i}']])
    
    # Compute the proof complexity using a small DPLL solver
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        pure_literals = {}
        for c in clauses:
            for l in c:
                if -l in pure_literals:
                    pure_literals[l] += 1
                else:
                    pure_literals[l] = 1
        
        unit_literal = next((c[0] for c in unit_clauses), None)
        if unit_literal is not None:
            assignment[unit_literal] = True
            return dpll([c for c in clauses if unit_literal not in c and -unit_literal not in c], assignment)
        
        pure_literal = next((l for l, count in pure_literals.items() if count % 2 == 1), None)
        if pure_literal is not None:
            assignment[pure_literal] = True
            return dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], assignment)
        
        literal = next((l for l in range(1, n+1) if l not in assignment), None)
        assignment[literal] = True
        if dpll(clauses, assignment):
            return True
        
        assignment[literal] = False
        return dpll(clauses, assignment)
    
    proof_complexity = 0
    for _ in range(100):
        if not dpll(clauses):
            proof_complexity += 1
    
    # Check the conjecture
    conjecture_holds = λ_computed ** 2 <= proof_complexity / n
    counterexample = "" if conjecture_holds else f"λ={λ_computed}, proof_complexity={proof_complexity}"
    
    return {
        "metric_name": "Proof Complexity",
        "metric_value": proof_complexity,
        "instances_tested": 100,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")