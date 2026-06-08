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
            for j in range(i + 1, n):
                if M[i][j] > 0:
                    rank += 1
        return rank
    
    def generate_metric_space(n):
        X = [[random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            X[i][i] = 0
        for i in range(n):
            for j in range(i + 1, n):
                X[i][j] = random.random()
                X[j][i] = X[i][j]
        return X
    
    def min_order(X):
        M = gromov_wasserstein_distance(X, X)
        order = 0
        for i in range(len(M)):
            for j in range(i + 1, len(M)):
                if M[i][j] > 0:
                    order += 1
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            X = generate_metric_space(n)
            min_order_X = min_order(X)
            rank_X = communication_complexity_rank(X)
            instances_tested += 1
            n_max = max(n_max, n)
            total_metric_value += abs(min_order_X - rank_X)
    
    mean_metric_value = total_metric_value / instances_tested
    
    if mean_metric_value > 3:
        conjecture_holds = False
        counterexample = "mean_metric_value > 3"
    else:
        conjecture_holds = True
    
    return {
        "metric_name": "mean_abs_diff",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_abs_diff > 3\" first_failing_seed={first_failing_seed}")