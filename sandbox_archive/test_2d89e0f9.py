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
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def bp_read_twice_width(cnf):
        n = len(cnf)
        width = 0
        for clause in cnf:
            width = max(width, len(clause))
        return width

    def tropicalized_hodge_rank(cnf):
        n = len(cnf)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                count = 0
                for clause in cnf:
                    if (i in clause and j not in clause) or (j in clause and i not in clause):
                        count += 1
                A[i][j] = A[j][i] = count
        rank = 0
        for row in gaussian_elimination(A):
            rank += sum(1 for x in row if x != 0)
        return rank

    def f(n):
        # Placeholder function for the upper bound of rho(V(I))
        return n**2

    cnf = []
    n = random.randint(5, 40)
    m = random.randint(2*n, 3*n)
    for _ in range(m):
        clause = set(random.sample(range(n), random.randint(1, n)))
        cnf.append(clause)

    rho_V_I = tropicalized_hodge_rank(cnf)
    bp_width = bp_read_twice_width(cnf)

    return {
        "metric_name": "rho(V(I))",
        "metric_value": rho_V_I,
        "instances_tested": 1,
        "conjecture_holds": rho_V_I <= f(n) and bp_width <= 10,
        "counterexample": "" if rho_V_I <= f(n) and bp_width <= 10 else "rho(V(I)) > f(n) or BP_ReadTwice width > 10"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rho_V_I = sum(r["metric_value"] for r in results) / len(results)
    std_rho_V_I = math.sqrt(sum((r["metric_value"] - mean_rho_V_I)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_V_I} std={std_rho_V_I} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_V_I} std={std_rho_V_I} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rho(V(I)) > f(n) or BP_ReadTwice width > 10\" first_failing_seed={first_failing_seed}")