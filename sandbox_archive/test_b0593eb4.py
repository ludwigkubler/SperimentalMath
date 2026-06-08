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
    
    def gromov_wasserstein_distance(X, Y):
        n = len(X)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d_ij = abs(X[i][j] - X[j][i])
                d_ji = abs(Y[i][j] - Y[j][i])
                M[i][j] = M[j][i] = max(d_ij, d_ji)
        return M
    
    def communication_complexity_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            row_sum = sum(M[i])
            col_sum = sum(M[j][i] for j in range(n))
            rank += max(row_sum, col_sum)
        return rank
    
    def generate_metric_space(n):
        points = [(random.random(), random.random()) for _ in range(n)]
        X = [[0] * n for _ in range(n)]
        Y = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d_ij = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
                X[i][j] = X[j][i] = d_ij
                Y[i][j] = Y[j][i] = d_ij
        return X, Y
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        n_max = n
        total_diff = 0
        
        for _ in range(5):  # Sample 5 instances per size
            X, Y = generate_metric_space(n)
            M = gromov_wasserstein_distance(X, Y)
            min_order_X = sum(sum(row) for row in M) / n
            rank_Y = communication_complexity_rank(M)
            
            diff = abs(min_order_X - rank_Y)
            total_diff += diff
            instances_tested += 1
        
        mean_diff = total_diff / instances_tested
        conjecture_holds = mean_diff <= 3
        counterexample = "" if conjecture_holds else f"mean_diff={mean_diff}"
        
        results.append({
            "metric_name": "mean_diff",
            "metric_value": mean_diff,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0],
        "mean_diff": sum(r["metric_value"] for r in results) / len(results),
        "support_fraction": sum(1 for r in results if r["conjecture_holds"]) / len(results)
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["mean_diff"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_diff exceeded 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")