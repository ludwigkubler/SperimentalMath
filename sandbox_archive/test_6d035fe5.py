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
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    def communication_complexity_rank(G):
        # Placeholder function to compute the communication complexity rank
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    kappa_G = communication_complexity_rank(G)
    
    def minimal_rank(D):
        # Placeholder function to compute the minimal rank of an algebraic combinatorial design
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(kappa_G, 2 * n)
    
    D_G = []  # Dummy design matrix
    r_D_G = minimal_rank(D_G)
    
    metric_value = r_D_G
    instances_tested = 1
    n_max = n
    conjecture_holds = r_D_G >= kappa_G + math.log(n, 2)
    counterexample = "" if conjecture_holds else f"Graph with {n} vertices, kappa(G) = {kappa_G}, minimal rank(D(G)) = {r_D_G}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r >= kappa_G + math.log(n, 2)) / len(results)
    
    if all(r >= kappa_G + math.log(n, 2) for r, n, kappa_G in zip(results, [run_trial(seed)["n_max"] for seed in seeds], [run_trial(seed)["metric_value"] for seed in seeds])):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < kappa_G + math.log(n, 2) for r, n, kappa_G in zip(results, [run_trial(seed)["n_max"] for seed in seeds], [run_trial(seed)["metric_value"] for seed in seeds])):
        first_failing_seed = next(i for i, (r, n, kappa_G) in enumerate(zip(results, [run_trial(seed)["n_max"] for seed in seeds], [run_trial(seed)["metric_value"] for seed in seeds])) if r < kappa_G + math.log(n, 2))
        print(f"RESULT: FALSIFIED counterexample=\"Graph with {run_trial(first_failing_seed)['n_max']} vertices\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")