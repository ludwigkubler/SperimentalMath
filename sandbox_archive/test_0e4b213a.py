# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def AND_3(x):
        return x[0] and x[1] and x[2]
    
    def MAJ_3(x):
        return sum(x) >= 2
    
    def PARITY_4(x):
        return sum(x) % 2 == 1
    
    def PARITY_5(x):
        return sum(x) % 2 == 1
    
    functions = [AND_3, MAJ_3, PARITY_4, PARITY_5]
    
    results = []
    for f in functions:
        n = random.choice([5, 8, 11, 14])
        X_f = [(i, j) for i in range(2**n) for j in range(2**n) if f(i) != f(j)]
        
        def d_f(x, y):
            for k in range(1, n+1):
                queries = []
                for i in range(n):
                    queries.append((i, x[i] ^ y[i]))
                if all(f(query[0]) == query[1] for query in queries):
                    return math.log2(k)
            return float('inf')
        
        def d_fA(x, y):
            if f(x) != f(y):
                return 1
            else:
                return float('inf')
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i+1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                factor = A[i][i]
                for j in range(n):
                    A[i][j] /= factor
                for j in range(m):
                    if j != i:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]
            return A
        
        def compute_roe_cohomology(d_f, n):
            G = [[d_f(i, j) for j in range(2**n)] for i in range(2**n)]
            delta = []
            for i in range(1, 2**n):
                row = [0] * (2**n)
                row[i-1] = -1
                for j in range(i+1, 2**n):
                    if d_f(i, j) == 1:
                        row[j-1] = 1
                delta.append(row)
            delta = gaussian_elimination(delta)
            rank = sum(1 for row in delta if any(x != 0 for x in row))
            return rank
        
        def compute_kappa_hat(f, d_f, n):
            max_value = float('-inf')
            for R in range(1, n+1):
                T = [[0] * (2**n) for _ in range(2**n)]
                for i in range(2**n):
                    for j in range(2**n):
                        if abs(d_f(i, j)) <= R:
                            T[i][j] = 1
                c = []
                for e in range(1, 2**n):
                    row = [0] * (2**n)
                    row[e-1] = -1
                    for f in range(e+1, 2**n):
                        if d_f(e, f) == 1:
                            row[f-1] = 1
                    c.append(row)
                c = gaussian_elimination(c)
                rank_c = sum(1 for row in c if any(x != 0 for x in row))
                value = math.log(abs(sum(T[i][j] * c[j][i] for i in range(2**n) for j in range(2**n)))) / math.log(R)
                max_value = max(max_value, value)
            return max_value
        
        d_f_values = [(x, y, d_f(x, y)) for x, y in X_f]
        d_fA_values = [(x, y, d_fA(x, y)) for x, y in X_f]
        
        HX1_fA = compute_roe_cohomology(d_fA, n)
        kappa_hat_f = compute_kappa_hat(f, d_f, n)
        kappa_hat_fA = compute_kappa_hat(lambda x: f(x), d_fA, n)
        
        results.append({
            "f": f.__name__,
            "n": n,
            "d_f_values": d_f_values,
            "d_fA_values": d_fA_values,
            "HX1_fA": HX1_fA,
            "kappa_hat_f": kappa_hat_f,
            "kappa_hat_fA": kappa_hat_fA
        })
    
    total_kappa_hat_f = sum(result["kappa_hat_f"] for result in results)
    total_kappa_hat_fA = sum(result["kappa_hat_fA"] for result in results)
    avg_kappa_hat_f = total_kappa_hat_f / len(results)
    avg_kappa_hat_fA = total_kappa_hat_fA / len(results)
    
    conjecture_holds = all(result["HX1_fA"] == 0 and result["kappa_hat_fA"] <= 2 for result in results) and any(result["kappa_hat_f"] > result["kappa_hat_fA"] + 0.5 for result in results)
    
    return {
        "metric_name": "κ̂",
        "metric_value": avg_kappa_hat_f,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"SEED": seed, **result}))
    
    avg_kappa_hat_f = sum(result["kappa_hat_f"] for result in results) / len(results)
    avg_kappa_hat_fA = sum(result["kappa_hat_fA"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["HX1_fA"] == 0 and result["kappa_hat_fA"] <= 2 and result["kappa_hat_f"] > result["kappa_hat_fA"] + 0.5) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_kappa_hat_f} std=0 support_fraction={support_fraction}")
    elif any(result["HX1_fA"] != 0 or result["kappa_hat_fA"] > 2 or result["kappa_hat_f"] <= result["kappa_hat_fA"] + 0.5 for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")