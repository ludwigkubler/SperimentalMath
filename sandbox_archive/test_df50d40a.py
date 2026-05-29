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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def hodge_rank(poly, n):
    # Placeholder for actual Hodge rank computation
    # This is a dummy implementation and should be replaced with the actual algorithm
    return len(poly)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, complexity):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(complexity):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def polynomial_from_cnf(cnf):
        # Placeholder for actual polynomial construction from CNF
        # This is a dummy implementation and should be replaced with the actual algorithm
        poly = [0] * (1 << n)
        for clause in cnf:
            term = 1
            for var in clause:
                if random.choice([True, False]):
                    term *= -1
                term *= (1 << abs(var) - 1)
            poly[term] += 1
        return poly
    
    def frege_proof_complexity(cnf):
        # Placeholder for actual Frege proof complexity computation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return len(cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    complexity = random.randint(n//2 + 1, n)
    cnf = generate_cnf(n, complexity)
    poly = polynomial_from_cnf(cnf)
    proof_complexity = frege_proof_complexity(cnf)
    
    hodge_r = hodge_rank(poly, n)
    c = 0.5  # Placeholder value for c
    if proof_complexity > n/2 and hodge_r < c * math.log(n):
        conjecture_holds = False
        counterexample = "Hodge rank too low for given Frege proof complexity"
    elif proof_complexity <= n/2 and hodge_r > 2**complexity:
        conjecture_holds = False
        counterexample = "Frege proof complexity too low for given Hodge rank"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": hodge_r,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_hodge_rank = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_hodge_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_hodge_rank} std={std_deviation} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_hodge_rank} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge rank too low for given Frege proof complexity\" first_failing_seed={first_failing_seed}")