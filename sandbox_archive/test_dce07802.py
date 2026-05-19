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
    
    def kronecker_product(A, B):
        m, n = len(A), len(A[0])
        p, q = len(B), len(B[0])
        result = [[0 for _ in range(n*q)] for _ in range(m*p)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    for l in range(q):
                        result[i*p + k][j*q + l] = A[i][j] * B[k][l]
        return result
    
    def matrix_rank(matrix, tol=1e-8):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            if all(abs(matrix[row][col]) < tol for row in range(m)):
                continue
            rank += 1
            pivot_row = next(row for row in range(m) if abs(matrix[row][col]) > tol)
            matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
            for other_col in range(n):
                if other_col != col:
                    factor = matrix[other_col][col] / matrix[col][col]
                    for row in range(m):
                        matrix[other_col][row] -= factor * matrix[col][row]
        return rank
    
    def build_cross_read_kronecker_sum(D):
        n = len(D)
        K = [[0 for _ in range(n*n)] for _ in range(n*n)]
        for i in range(n):
            for j in range(n):
                p1, p2 = 2*i + (j % 2), 2*j + (i % 2)
                Kronecker_product(D[p1], D[p2])
                K = kronecker_product(K, Kronecker_product(D[p1], D[p2]))
        return K
    
    def build_read_twice_bp(n):
        w = 2**n
        T_p_b = [[[random.randint(0, 1) for _ in range(w)] for _ in range(w)] for _ in range(4*n)]
        D_p = [T_p_1 - T_p_0 for T_p_1, T_p_0 in zip(T_p_b[::2], T_p_b[1::2])]
        return D_p
    
    def build_random_bp(n):
        w = 2**n
        T_p_b = [[[random.randint(0, 1) for _ in range(w)] for _ in range(w)] for _ in range(4*n)]
        D_p = [T_p_1 - T_p_0 for T_p_1, T_p_0 in zip(T_p_b[::2], T_p_b[1::2])]
        return D_p
    
    def compute_rho(n):
        D_ip2 = build_read_twice_bp(n)
        K_ip2 = build_cross_read_kronecker_sum(D_ip2)
        rho_ip2 = matrix_rank(K_ip2)
        
        D_rand = build_random_bp(n)
        K_rand = build_cross_read_kronecker_sum(D_rand)
        rho_rand = matrix_rank(K_rand)
        
        return rho_ip2, rho_rand
    
    n_values = [2, 3, 4, 5]
    rho_ip2_total = 0
    rho_rand_total = 0
    instances_tested = 0
    
    for n in n_values:
        rho_ip2, rho_rand = compute_rho(n)
        rho_ip2_total += rho_ip2
        rho_rand_total += rho_rand
        instances_tested += 1
        
        if rho_ip2 < 2**n / 4:
            return {
                "metric_name": "rho",
                "metric_value": (rho_ip2, rho_rand),
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"IP_2 BP with n={n} has rho(P) < 2^n/4"
            }
    
    mean_rho_ip2 = rho_ip2_total / instances_tested
    mean_rho_rand = rho_rand_total / instances_tested
    
    return {
        "metric_name": "rho",
        "metric_value": (mean_rho_ip2, mean_rho_rand),
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30))
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    rho_ip2_values = [r["metric_value"][0] for r in results if "metric_value" in r]
    rho_rand_values = [r["metric_value"][1] for r in results if "metric_value" in r]
    
    mean_rho_ip2 = sum(rho_ip2_values) / len(rho_ip2_values)
    std_rho_ip2 = (sum((x - mean_rho_ip2)**2 for x in rho_ip2_values) / len(rho_ip2_values))**0.5
    fraction_supporting = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"])
    
    if fraction_supporting >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_ip2} std={std_rho_ip2} support_fraction={fraction_supporting}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")