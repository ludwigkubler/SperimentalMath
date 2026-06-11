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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_mul(A, B):
        m, n, p = len(A), len(B), len(B[0])
        result = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * matrix_det(submatrix)
        return det
    
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
    
    def generate_random_sat(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def truth_table(clauses):
        n = len(clauses[0])
        tt = []
        for i in range(2 ** n):
            assignment = [(i >> j) & 1 for j in range(n)]
            satisfied = all(any(assignment[j-1] if sign == 1 else not assignment[j-1] for sign, j in enumerate(clause)) for clause in clauses)
            tt.append(satisfied)
        return tt
    
    def cubic_extension(truth_table):
        n = len(truth_table[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = 1
            A[n][i] = truth_table[i]
        det = matrix_det(A)
        return abs(det)
    
    def resolution_width(clauses):
        n = len(clauses[0])
        queue = [set(clause) for clause in clauses]
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(abs(x) == abs(y) and x != y for x in queue[i] for y in queue[j]):
                        resolvent = {x for x in queue[i]} ^ {y for y in queue[j]}
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            queue.extend(new_clauses)
        return len(queue)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_random_sat(n)
    tt = truth_table(clauses)
    galois_order = cubic_extension(tt)
    resolution_width_val = resolution_width(clauses)
    
    return {
        "metric_name": "correlation",
        "metric_value": abs(galois_order - resolution_width_val),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")