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
    
    def matrix_multiply(A, B):
        return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
    
    def matrix_power(M, k):
        result = M
        for _ in range(1, k):
            result = matrix_multiply(result, M)
        return result
    
    def trace(matrix):
        return sum(matrix[i][i] for i in range(len(matrix)))
    
    def frobenius_norm(matrix):
        return math.sqrt(sum(sum(x**2 for x in row) for row in matrix))
    
    def power_iteration(B, num_steps=50):
        v = [random.random() for _ in range(len(B))]
        v /= frobenius_norm(v)
        for _ in range(num_steps):
            v = matrix_multiply(B, v)
            v /= frobenius_norm(v)
        return v
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def free_cumulant_4(M):
        B = matrix_multiply(M, M)
        B2 = matrix_multiply(B, B)
        B3 = matrix_multiply(B2, B)
        
        s1 = trace(B) / len(M)**2
        s2 = frobenius_norm(B)**2 / len(M)**3
        s3 = trace(matrix_multiply(B2, B)) / len(M)**4
        s4 = frobenius_norm(B2)**2 / len(M)**5
        
        kappa_2 = s2 - s1**2
        kappa_4 = s4 - 4 * s1 * s3 - 2 * s2**2 + 10 * s1**2 * s2 - 5 * s1**4
        
        return kappa_4
    
    def stable_rank(M):
        B = matrix_multiply(M, M)
        eigenvector = power_iteration(B)
        sigma_1 = sum(eigenvector[i]**2 for i in range(len(eigenvector)))
        return trace(B) / (sigma_1 * frobenius_norm(B))
    
    def bridge_invariant(M):
        kappa_4 = free_cumulant_4(M)
        sr = stable_rank(M)
        term1 = log2(abs(kappa_4) / (kappa_2**2 + len(M)**(-2)))
        term2 = log2(sr)
        return min(term1, term2)
    
    def generate_disj_matrix(n):
        M1 = [[1, 1], [1, 0]]
        result = M1
        for _ in range(1, n):
            result = matrix_multiply(result, M1)
        return result
    
    def generate_random_sign_matrix(N):
        return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    
    def generate_low_rank_decoy(N, k):
        u = [random.random() for _ in range(k)]
        v = [random.random() for _ in range(k)]
        return [[u[i] * v[j] for j in range(N)] for i in range(N)]
    
    def generate_hadamard_matrix(N):
        if N == 1:
            return [[1]]
        H_half = generate_hadamard_matrix(N // 2)
        H = [[0] * N for _ in range(N)]
        for i in range(N // 2):
            for j in range(N // 2):
                H[i][j] = H_half[i][j]
                H[i][j + N // 2] = H_half[i][j]
                H[i + N // 2][j] = H_half[i][j]
                H[i + N // 2][j + N // 2] = -H_half[i][j]
        return H
    
    def generate_ip2_matrix(N):
        if N == 1:
            return [[1]]
        I = [[0] * N for _ in range(N)]
        for i in range(N):
            I[i][i] = 1
        J = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if i != j:
                    J[i][j] = 1
        return matrix_multiply(I, J)
    
    def communication_complexity_upper_bound(M):
        rank_M = sum(1 for row in M if any(x != 0 for x in row))
        return max(math.ceil(math.log2(len(M))), math.ceil(math.log2(rank_M))) + 2
    
    def run_disj_trial(n):
        M = generate_disj_matrix(n)
        tau = bridge_invariant(M)
        cc_upper_bound = communication_complexity_upper_bound(M)
        if tau < 0.15 * n or 0.05 * tau > cc_upper_bound:
            return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"DISJ_{n}"}
        return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}
    
    def run_random_trial(N):
        M = generate_random_sign_matrix(N)
        tau = bridge_invariant(M)
        cc_upper_bound = communication_complexity_upper_bound(M)
        if 0.05 * tau > min(math.ceil(math.log2(N)), math.ceil(math.log2(rank_M))) + 2:
            return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"random_{N}"}
        return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}
    
    def run_low_rank_trial(N, k):
        M = generate_low_rank_decoy(N, k)
        tau = bridge_invariant(M)
        cc_upper_bound = communication_complexity_upper_bound(M)
        if 0.05 * tau > min(math.ceil(math.log2(N)), math.ceil(math.log2(rank_M))) + 2:
            return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"low_rank_{N}_{k}"}
        return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}
    
    def run_hadamard_trial(N):
        M = generate_hadamard_matrix(N)
        tau = bridge_invariant(M)
        cc_upper_bound = communication_complexity_upper_bound(M)
        if 0.05 * tau > min(math.ceil(math.log2(N)), math.ceil(math.log2(rank_M))) + 2:
            return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"hadamard_{N}"}
        return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}
    
    def run_ip2_trial(N):
        M = generate_ip2_matrix(N)
        tau = bridge_invariant(M)
        cc_upper_bound = communication_complexity_upper_bound(M)
        if 0.05 * tau > min(math.ceil(math.log2(N)), math.ceil(math.log2(rank_M))) + 2:
            return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"ip2_{N}"}
        return {"metric_name": "tau", "metric_value": tau, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}
    
    results = []
    for n in range(2, 10):
        results.append(run_disj_trial(n))
    
    for N in [4, 8, 16, 32, 64, 128, 256]:
        for _ in range(30):
            results.append(run_random_trial(N))
    
    for N in [128]:
        for k in [1, 2, 4, 8, 16, 32]:
            results.append(run_low_rank_trial(N, k))
    
    for N in [16, 64, 256]:
        results.append(run_hadamard_trial(N))
        results.append(run_ip2_trial(N))
    
    tau_disj_values = [result["metric_value"] for result in results if "tau" in result and result["counterexample"] == ""]
    cc_upper_bounds = [communication_complexity_upper_bound(generate_random_sign_matrix(N)) for N in range(4, 513)]
    
    mean_tau = sum(tau_disj_values) / len(tau_disj_values)
    std_tau = math.sqrt(sum((x - mean_tau)**2 for x in tau_disj_values) / len(tau_disj_values))
    support_fraction = sum(result["conjecture_holds"] for result in results if "tau" in result and result["counterexample"] == "") / len(results)
    
    if all(0.15 * n <= tau for n, tau in zip(range(2, 10), tau_disj_values)):
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_tau} std={std_tau} support_fraction={support_fraction}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if "tau" in result and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"DISJ\" first_failing_seed={first_failing_seed}")

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")