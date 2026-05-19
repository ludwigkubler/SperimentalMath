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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_rank(A, tol=1e-8):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(abs(x) > tol for x in row):
                rank += 1
        return rank
    
    def kronecker_product(A, B):
        m, n = len(A), len(A[0])
        p, q = len(B), len(B[0])
        result = [[0] * (n * q) for _ in range(m * p)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    for l in range(q):
                        result[i * p + k][j * q + l] = A[i][j] * B[k][l]
        return result
    
    def build_read_twice_bp(n, is_ip2=True):
        w = 1 << n
        T = [[[0] * w for _ in range(w)] for _ in range(4 * n)]
        if is_ip2:
            for p in range(4 * n):
                for v in range(2 * n):
                    if (v // 2) % 2 == p % 2:
                        T[p][v % 2][v // 2] = 1
                    else:
                        T[p][v % 2][v // 2] = -1
        else:
            for p in range(4 * n):
                for v in range(2 * n):
                    T[p][v % 2][v // 2] = random.randint(0, 1)
        return T
    
    def build_bit_flip_operators(T):
        w = len(T[0])
        D = [[0] * w for _ in range(w)]
        for p in range(len(T)):
            for b in range(2):
                for i in range(w):
                    for j in range(w):
                        if T[p][b][i] == 1 and T[p][b][j] == 1:
                            D[i][j] += 1
                        elif T[p][b][i] == 0 and T[p][b][j] == 0:
                            D[i][j] -= 1
        return D
    
    def build_cross_read_kronecker_sum(D):
        w = len(D)
        K = [[0] * (w ** 2) for _ in range(w ** 2)]
        for v in range(2 * n):
            p1, p2 = v // 2, v // 2 + n
            K = kronecker_product(K, kronecker_product(D[p1], D[p2]))
        return K
    
    def compute_rho(P):
        T = build_read_twice_bp(n, is_ip2=True)
        D = build_bit_flip_operators(T)
        K = build_cross_read_kronecker_sum(D)
        return matrix_rank(K)
    
    n_values = [2, 3, 4, 5]
    rho_ip2_values = []
    rho_rand_values = []
    
    for n in n_values:
        rho_ip2 = compute_rho(n)
        rho_ip2_values.append(rho_ip2 / (2 ** n))
        
        T = build_read_twice_bp(n, is_ip2=False)
        D = build_bit_flip_operators(T)
        K = build_cross_read_kronecker_sum(D)
        rho_rand = matrix_rank(K)
        rho_rand_values.append(rho_rand / (2 ** n))
    
    median_rho_ip2 = sorted(rho_ip2_values)[len(rho_ip2_values) // 2]
    median_rho_rand = sorted(rho_rand_values)[len(rho_rand_values) // 2]
    
    if any(rho < 2 ** n / 4 for rho, n in zip(rho_ip2_values, n_values)):
        return {
            "metric_name": "rho(P_IP2)",
            "metric_value": median_rho_ip2,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": "rho(P_IP2) < 2^n/4 for some n"
        }
    
    if median_rho_ip2 / 2 ** n >= 0.25 and median_rho_ip2 / median_rho_rand >= 3:
        return {
            "metric_name": "rho(P_IP2)",
            "metric_value": median_rho_ip2,
            "instances_tested": len(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    return {
        "metric_name": "rho(P_IP2)",
        "metric_value": median_rho_ip2,
        "instances_tested": len(n_values),
        "conjecture_holds": False,
        "counterexample": "median rho(P_IP2)/2^n < 0.25 or median ratio rho(P_IP2)/rho(P_rand) < 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(30))
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    rho_ip2_values = [r["metric_value"] for r in results]
    median_rho_ip2 = sorted(rho_ip2_values)[len(rho_ip2_values) // 2]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={median_rho_ip2} std=0.0 support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='rho(P_IP2) < 2^n/4 for some n' first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE reason=support_fraction={support_fraction}")