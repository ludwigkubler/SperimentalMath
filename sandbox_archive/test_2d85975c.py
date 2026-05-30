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

def generate_random_boolean_matrix(N):
    return [[random.choice([0, 1]) for _ in range(N)] for _ in range(N)]

def hyperbolic_metric_diameter(M):
    N = len(M)
    max_distance = 0
    for i in range(N):
        for j in range(i + 1, N):
            distance = sum(abs(M[i][k] - M[j][k]) for k in range(N))
            if distance > max_distance:
                max_distance = distance
    return max_distance

def randomized_two_party_communication_complexity(M):
    N = len(M)
    def simulate_protocol():
        sender_bits = random.randint(0, 2**N - 1)
        receiver_bits = 0
        for i in range(N):
            if M[i][sender_bits & 1] == 1:
                receiver_bits |= (1 << i)
            sender_bits >>= 1
        return len(bin(receiver_bits)) - 2
    return sum(simulate_protocol() for _ in range(100)) / 100

def spearman_rank_correlation(X, Y):
    n = len(X)
    rank_X = {x: i + 1 for i, x in enumerate(sorted(set(X)))}
    rank_Y = {y: i + 1 for i, y in enumerate(sorted(set(Y)))}
    sum_dX2 = sum((rank_X[X[i]] - rank_X[Y[i]]) ** 2 for i in range(n))
    sum_dY2 = sum((rank_Y[Y[i]] - rank_Y[X[i]]) ** 2 for i in range(n))
    return 1 - (6 * sum_dX2 + 6 * sum_dY2) / (n * (n**2 - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    d_H_values = []
    CC_R_values = []
    
    for n in n_values:
        M = generate_random_boolean_matrix(n)
        d_H = hyperbolic_metric_diameter(M)
        CC_R = randomized_two_party_communication_complexity(M)
        d_H_values.append(d_H)
        CC_R_values.append(CC_R)
    
    rho = spearman_rank_correlation(d_H_values, CC_R_values)
    mean_rho = sum(rho) / len(rho)
    std_rho = math.sqrt(sum((r - mean_rho) ** 2 for r in rho) / len(rho))
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": mean_rho,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": mean_rho >= 0.8 and std_rho <= 3,
        "counterexample": "" if mean_rho >= 0.8 and std_rho <= 3 else "rho_out_of_bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho_out_of_bounds' first_failing_seed={first_failing_seed}")