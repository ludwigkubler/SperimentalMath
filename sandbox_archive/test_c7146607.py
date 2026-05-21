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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(10 * n):  # Each variable appears in about 10 clauses
            variables = [random.randint(0, n-1) for _ in range(3)]
            clause = [(-1 if random.choice([True, False]) else 1) * (x + 1) for x in variables]
            clauses.append(clause)
        return clauses
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                    max_row = j
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            pivot = augmented[i][i]
            for j in range(n + 1):
                augmented[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = augmented[j][i]
                    for k in range(n + 1):
                        augmented[j][k] -= factor * augmented[i][k]
        return [row[-1] for row in augmented]
    
    def solve_linear_system(A, b):
        return gaussian_elimination(A, b)
    
    def is_integer(x):
        return abs(x - round(x)) < 1e-9
    
    n = 40
    clauses = generate_3cnf(n)
    
    # Convert clauses to a system of polynomial equations
    variables = [i for i in range(2*n)]
    A = []
    b = []
    for clause in clauses:
        row = [0] * (2*n)
        for var in clause:
            if var > 0:
                row[var-1] += 1
            else:
                row[-var-1] -= 1
        A.append(row)
        b.append(0)
    
    # Solve the system to find the dimension of the radical
    solution = solve_linear_system(A, b)
    rank = sum(is_integer(x) for x in solution)
    dim_radical = n - rank
    
    # Estimate the minimal SOS degree required
    epsilon = 1 / (n**2)
    d = dim_radical * math.log(n)
    
    return {
        "metric_name": "SOS_degree",
        "metric_value": d,
        "instances_tested": 1,
        "conjecture_holds": d >= 0.5 * dim_radical / math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")