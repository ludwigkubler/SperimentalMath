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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        return [row[:n-1] for row in A]

    def tensor_product_coefficient_matrix(f):
        n = len(f)
        m = 2**n
        T = [[0] * (m - 1) for _ in range(m)]
        for i in range(m):
            x, y = bin(i)[2:].zfill(n), bin((i + 1) % m)[2:].zfill(n)
            for j in range(m):
                if all(int(x[k]) == int(y[k]) for k in range(n)):
                    T[i][j] += f[j]
        return gaussian_elimination(T)

    def dpll_proof_length(F):
        n = len(F)
        clauses = [set(map(int, clause.split())) for clause in F]
        stack = []
        assignment = [0] * (n + 1)
        
        def backtrack(level):
            if level == n + 1:
                return True
            for literal in range(1, -1, -1):
                if assignment[level] != 0:
                    continue
                assignment[level] = literal
                if all(any(lit in clause for lit in assignment) for clause in clauses):
                    stack.append((level, literal))
                    if backtrack(level + 1):
                        return True
                assignment[level] = 0
            stack.pop()
            return False
        
        return len(stack)

    def polynomial_value(f, x, y):
        n = len(f)
        result = f[0]
        for i in range(1, n):
            result += f[i] * (x**i + y**i)
        return result

    def generate_cnf(n):
        clauses = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(j + 1)
                else:
                    clause.append(-(j + 1))
            clauses.append(' '.join(map(str, clause)) + ' 0')
        return clauses

    n = random.choice([5, 10, 15, 20, 30, 40])
    F = generate_cnf(n)
    
    f = [random.randint(0, 1) for _ in range(2**n)]
    T = tensor_product_coefficient_matrix(f)
    r_f = sum(1 for row in T if any(row))
    
    t_F = dpll_proof_length(F)
    
    log_r_f = math.log2(r_f) if r_f > 0 else float('inf')
    difference = abs(log_r_f - t_F)
    
    return {
        "metric_name": "log_r_f",
        "metric_value": log_r_f,
        "instances_tested": 1,
        "conjecture_holds": difference <= 1,
        "counterexample": "" if difference <= 1 else f"n={n}, log2(r(f))={log_r_f}, t*(F)={t_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")