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

def hamming_weight(x):
    return bin(x).count('1')

def sparse_matmul(A, B):
    C = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                if A[i][k] != 0 and B[k][j] != 0:
                    C[i][j] += A[i][k] * B[k][j]
    return C

def sparse_trace(A):
    return sum(A[i][i] for i in range(len(A)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        X_f = [tuple(random.randint(0, 1) for _ in range(2*n)) for _ in range(2**n)]
        f_inv_0 = [x for x in X_f if sum(x) % 2 == 0]
        f_inv_1 = [x for x in X_f if sum(x) % 2 == 1]
        
        d_f = [[math.log2(hamming_weight(x^y)) for y in X_f] for x in X_f]
        c_IP = [[(-1)**(sum(x[i]^y[i] for i in range(2*n)) % 2) for y in X_f] for x in X_f]
        
        T_Rs = []
        for R in range(1, int(math.log2(2*n)) + 1):
            B_R = [[1 if d_f[i][j] <= R else 0 for j in range(len(X_f))] for i in range(len(X_f))]
            ball_volume = sum(sum(row) for row in B_R)
            T_R = [[B_R[i][j] / (1 + ball_volume) for j in range(len(X_f))] for i in range(len(X_f))]
            T_Rs.append(T_R)
        
        p_Rs = [sparse_trace(sparse_matmul(c_IP, T)) for T in T_Rs]
        log_p_Rs = [math.log(abs(p)) if p != 0 else -100 for p in p_Rs]
        
        alpha_n = sum(log_p_Rs) / len(log_p_Rs)
        results.append({"n": n, "alpha_n": alpha_n})
    
    random.seed(seed)
    f_prime_inv_0 = [tuple(random.randint(0, 1) for _ in range(2*n)) for _ in range(2**n)]
    f_prime_inv_1 = [x for x in X_f if sum(x) % 2 == 1]
    
    d_f_prime = [[math.log2(hamming_weight(x^y)) for y in X_f] for x in X_f]
    c_IP_prime = [[(-1)**(sum(x[i]^y[i] for i in range(2*n)) % 2) for y in X_f] for x in X_f]
    
    T_Rs_prime = []
    for R in range(1, int(math.log2(2*n)) + 1):
        B_R = [[1 if d_f_prime[i][j] <= R else 0 for j in range(len(X_f))] for i in range(len(X_f))]
        ball_volume = sum(sum(row) for row in B_R)
        T_R_prime = [[B_R[i][j] / (1 + ball_volume) for j in range(len(X_f))] for i in range(len(X_f))]
        T_Rs_prime.append(T_R_prime)
    
    p_Rs_prime = [sparse_trace(sparse_matmul(c_IP_prime, T)) for T in T_Rs_prime]
    log_p_Rs_prime = [math.log(abs(p)) if p != 0 else -100 for p in p_Rs_prime]
    
    alpha_n_prime_mean = sum(log_p_Rs_prime) / len(log_p_Rs_prime)
    alpha_n_prime_ci = 1.96 * math.sqrt(sum((x - alpha_n_prime_mean)**2 for x in log_p_Rs_prime) / (len(log_p_Rs_prime) - 1))
    
    conjecture_holds = all(alpha_n >= 0.7 for alpha_n in [r["alpha_n"] for r in results]) and \
                        all(results[i]["alpha_n"] <= results[i+1]["alpha_n"] for i in range(len(results)-1)) and \
                        alpha_n_prime_ci < 0.4
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "alpha_n",
        "metric_value": alpha_n,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    alpha_n_values = [r["alpha_n"] for r in results]
    alpha_n_mean = sum(alpha_n_values) / len(alpha_n_values)
    alpha_n_std = math.sqrt(sum((x - alpha_n_mean)**2 for x in alpha_n_values) / len(alpha_n_values))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={alpha_n_mean} std={alpha_n_std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")