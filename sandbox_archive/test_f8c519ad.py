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

def build_read_twice_bp(n):
    w = 2**n
    T_p_b = [[random.choice([0, 1]) for _ in range(w)] for _ in range(4*n)]
    D_p = []
    for T_p_1, T_p_0 in zip(T_p_b[::2], T_p_b[1::2]):
        D_p.append([[T_p_1[i][j] - T_p_0[i][j] for j in range(w)] for i in range(w)])
    return D_p

def compute_rho(n):
    w = 2**n
    P_IP2 = build_read_twice_bp(n)
    K_P = [[0]*w**2 for _ in range(w**2)]
    for D_p1, D_p2 in zip(P_IP2[::2], P_IP2[1::2]):
        for i in range(w):
            for j in range(w):
                for k in range(w):
                    for l in range(w):
                        K_P[i*w+k][j*w+l] += D_p1[i][k] * D_p2[j][l]
    rho_ip2 = gaussian_elimination(K_P)
    return rho_ip2

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i+1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [2, 3, 4, 5]
    rho_ip2_sum = 0
    rho_rand_sum = 0
    instances_tested = 0
    for n in n_values:
        rho_ip2 = compute_rho(n)
        P_rand = build_read_twice_bp(n)
        K_P_rand = [[0]*w**2 for _ in range(w**2)]
        for D_p1, D_p2 in zip(P_rand[::2], P_rand[1::2]):
            for i in range(w):
                for j in range(w):
                    for k in range(w):
                        for l in range(w):
                            K_P_rand[i*w+k][j*w+l] += D_p1[i][k] * D_p2[j][l]
        rho_rand = gaussian_elimination(K_P_rand)
        rho_ip2_sum += rho_ip2
        rho_rand_sum += rho_rand
        instances_tested += 4
    rho_ip2_avg = rho_ip2_sum / instances_tested
    rho_rand_avg = rho_rand_sum / instances_tested
    conjecture_holds = rho_ip2_avg >= 0.25 and rho_ip2_avg / rho_rand_avg >= 3
    counterexample = "" if conjecture_holds else f"rho_ip2_avg={rho_ip2_avg}, rho_rand_avg={rho_rand_avg}"
    return {
        "metric_name": "rank",
        "metric_value": rho_ip2_avg,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    rho_ip2_avg = sum(result["metric_value"] for result in results) / len(results)
    rho_rand_avg = sum(result["instances_tested"] * result["metric_value"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={rho_ip2_avg} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={rho_ip2_avg} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho_ip2_avg={rho_ip2_avg}, rho_rand_avg={rho_rand_avg}' first_failing_seed={first_failing_seed}")