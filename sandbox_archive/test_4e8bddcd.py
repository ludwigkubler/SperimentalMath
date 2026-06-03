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

def matrix_mult(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= 2
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] // A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) // A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        if not cnf:
            return True
        if any(len(clause) == 0 for clause in cnf):
            return False
        unit_clauses = [clause[0] for clause in cnf if len(clause) == 1]
        pure_symbols = set()
        for clause in cnf:
            for lit in clause:
                if -lit in pure_symbols:
                    pure_symbols.remove(-lit)
                else:
                    pure_symbols.add(lit)
        for lit in unit_clauses + list(pure_symbols):
            new_cnf = []
            for clause in cnf:
                if lit not in clause and -lit not in clause:
                    new_cnf.append(clause)
            if dpll(new_cnf):
                return True
        return False
    
    def tropical_motivic_rank(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        A = [[0]*n for _ in range(n)]
        b = [0]*n
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    A[lit-1][lit-1] += 1
                else:
                    A[-lit-1][-lit-1] += 1
            b[abs(clause[0])-1] += 1
        x = gaussian_elimination(A, b)
        return sum(x[i] for i in range(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        rank = tropical_motivic_rank(cnf)
        depth = dpll(cnf)
        results.append((rank, depth))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_depth = sum(depth for _, depth in results) / len(results)
    correlation = 0
    for (rank1, depth1), (rank2, depth2) in zip(results[:-1], results[1:]):
        correlation += (rank1 - mean_rank) * (depth2 - mean_depth)
    correlation /= (len(results)-1) * math.sqrt(sum((rank - mean_rank)**2 for rank, _ in results)) * math.sqrt(sum((depth - mean_depth)**2 for _, depth in results))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.7 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation\" first_failing_seed={first_failing_seed}")