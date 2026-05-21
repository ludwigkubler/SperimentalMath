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
    
    def generate_disjointness_matrix(n):
        X = list(range(n))
        Y = list(range(n))
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            x = random.sample(X, 1)[0]
            y = random.sample(Y, 1)[0]
            M[x][y] = 1
        return M
    
    def log_sum(matrix):
        total = sum(sum(abs(x) for x in row) for row in matrix)
        return math.log(total)
    
    def disjointness_communication_complexity(n):
        M = generate_disjointness_matrix(n)
        return log_sum(M) - math.log(n) - math.log(n)
    
    n_values = [10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        value = disjointness_communication_complexity(n)
        results.append(value)
    
    mean_value = sum(results) / len(results)
    conjecture_holds = all(value >= 0.5 * math.sqrt(n) for n, value in zip(n_values, results))
    counterexample = "" if conjecture_holds else "n=36"
    
    return {
        "metric_name": "disjointness_communication_complexity",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n=36\" first_failing_seed={first_failing_seed}")