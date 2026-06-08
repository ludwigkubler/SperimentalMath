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
    
    def gromov_wasserstein_distance(X):
        n = len(X)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d = sum(abs(x - y) for x, y in zip(X[i], X[j]))
                D[i][j] = D[j][i] = d
        return D
    
    def communication_complexity_rank(D):
        n = len(D)
        rank = 0
        while True:
            found = False
            for i in range(n):
                if all(D[i][j] == 0 for j in range(n) if j != i):
                    rank += 1
                    D[i] = [0] * n
                    found = True
                    break
            if not found:
                break
        return rank
    
    def min_order(X):
        D = gromov_wasserstein_distance(X)
        n = len(D)
        order = 0
        while True:
            found = False
            for i in range(n):
                if all(D[i][j] == 0 for j in range(n) if j != i):
                    order += 1
                    D[i] = [0] * n
                    found = True
                    break
            if not found:
                break
        return order
    
    def generate_metric_space(n):
        points = [[random.random() for _ in range(2)] for _ in range(n)]
        return points
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_diff = 0
        
        while len(results) < 30:
            X = generate_metric_space(n)
            min_order_X = min_order(X)
            rank_X = communication_complexity_rank(gromov_wasserstein_distance(X))
            
            diff = abs(min_order_X - rank_X)
            if diff > 3:
                counterexample = f"n={n}, min_order={min_order_X}, rank={rank_X}"
                return {
                    "metric_name": "diff",
                    "metric_value": diff,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            
            results.append(diff)
            instances_tested += 1
        
        mean_diff = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean_diff) ** 2 for x in results) / len(results))
        
        if all(diff <= 3 for diff in results):
            return {
                "metric_name": "diff",
                "metric_value": mean_diff,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": True,
                "counterexample": ""
            }
        else:
            counterexample = f"n={n}, min_order={min(results)}, rank={max(results)}"
            return {
                "metric_name": "diff",
                "metric_value": mean_diff,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": counterexample
            }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_diff) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        counterexample_desc = ", ".join(result["counterexample"] for result in results if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")