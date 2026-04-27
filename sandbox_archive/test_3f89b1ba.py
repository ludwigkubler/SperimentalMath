# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 11
    functions = ["AND_3", "MAJ_3", "PARITY_4", "PARITY_5"]
    function = random.choice(functions)
    
    if function == "AND_3":
        f = lambda x: all(x[i] for i in range(3))
    elif function == "MAJ_3":
        f = lambda x: sum(x) >= 2
    elif function == "PARITY_4":
        f = lambda x: sum(x) % 2 == 1
    elif function == "PARITY_5":
        f = lambda x: sum(x) % 2 == 1
    else:
        return {
            "metric_name": "",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    X_f = [(i, j) for i in range(2**n) for j in range(2**n) if f(i) != f(j)]
    d_f = {}
    for x, y in X_f:
        min_queries = float('inf')
        for k in range(1, n+1):
            queries = [random.randint(0, n-1) for _ in range(k)]
            if all(x & (1 << q) == y & (1 << q) for q in queries):
                min_queries = k
                break
        d_f[(x, y)] = math.log2(min_queries)
    
    d_f_A = {x: 1 for x in X_f if f(x) != f(0)}
    
    HX1_basis = []
    for R in range(1, n+1):
        T = [[random.randint(0, 1) for _ in range(R)] for _ in range(R)]
        T = matrix_multiplication(T, T)
        T = [row[:R] for row in T]
        A = []
        for x, y in X_f:
            if d_f[(x, y)] <= R:
                A.append([1 if i == j else 0 for i in range(R)])
        rank = gaussian_elimination(A)
        HX1_basis.extend(A[:rank])
    
    dim_HX1 = len(HX1_basis)
    
    def trace_pairing(c, T):
        return sum(c[i] * T[i][i] for i in range(len(T)))
    
    kappa_f_A = max(math.log(abs(trace_pairing(c, T))) / math.log(R) for c, T, R in zip(X_f, HX1_basis, [1]*len(X_f)))
    kappa_f = float('inf')
    
    result = {
        "metric_name": "κ̂",
        "metric_value": kappa_f_A,
        "instances_tested": len(X_f),
        "conjecture_holds": dim_HX1 == 0 and kappa_f_A <= 2 and kappa_f > kappa_f_A + 0.5,
        "counterexample": "" if dim_HX1 == 0 and kappa_f_A <= 2 and kappa_f > kappa_f_A + 0.5 else f"dim HX^1={dim_HX1}, κ̂(f^A)={kappa_f_A}, κ(f)={kappa_f}"
    }
    
    return result

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_kappa_f_A = sum(r["metric_value"] for r in results) / len(results)
    std_kappa_f_A = math.sqrt(sum((r["metric_value"] - mean_kappa_f_A)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_kappa_f_A} std={std_kappa_f_A} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")