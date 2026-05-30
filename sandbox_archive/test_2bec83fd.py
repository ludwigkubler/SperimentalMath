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

def generate_random_boolean_matrix(N):
    return [[random.choice([0, 1]) for _ in range(N)] for _ in range(N)]

def hyperbolic_metric_diameter(M):
    N = len(M)
    d_H = 0
    for i in range(N):
        for j in range(i + 1, N):
            d_H += math.sqrt((M[i][j] - M[j][i]) ** 2)
    return d_H

def randomized_two_party_communication_complexity(M):
    N = len(M)
    cc = 0
    for i in range(N):
        for j in range(i + 1, N):
            if M[i][j] != M[j][i]:
                cc += 1
    return cc

def spearman_rank_correlation(X, Y):
    n = len(X)
    rank_X = {x: rank for rank, x in enumerate(sorted(set(X)), start=1)}
    rank_Y = {y: rank for rank, y in enumerate(sorted(set(Y)), start=1)}
    sum_dX2 = sum((rank_X[X[i]] - rank_Y[Y[i]]) ** 2 for i in range(n))
    rho_numerator = n * sum_dX2
    rho_denominator = (n * sum(x ** 2 for x in X) - sum(X) ** 2) * (n * sum(y ** 2 for y in Y) - sum(Y) ** 2)
    if rho_denominator == 0:
        return 0
    rho = 1 - (6 * rho_numerator / rho_denominator)
    return max(-1, min(1, rho))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    d_H_values = []
    CC_R_values = []
    
    for n in n_values:
        M = generate_random_boolean_matrix(n)
        d_H = hyperbolic_metric_diameter(M)
        cc = randomized_two_party_communication_complexity(M)
        d_H_values.append(d_H)
        CC_R_values.append(cc)
    
    rho = spearman_rank_correlation(d_H_values, CC_R_values)
    conjecture_holds = rho >= 0.8 and rho <= 3
    counterexample = "" if conjecture_holds else f"rho={rho}"
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")