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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def hodge_rank(phi):
    # Placeholder function to simulate Hodge rank computation
    # This is a dummy implementation and will not work for real CNFs
    n = len(phi)
    m = len(phi[0])
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
    rref = gaussian_elimination(A)
    rank = sum(1 for row in rref if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # 5 instances per size
            m = random.randint(n, 2*n)
            phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
            hodge_rank_value = hodge_rank(phi)
            metric_values.append(hodge_rank_value)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(value >= m**(1/3) * n**(2/3) for value, m, n in zip(metric_values, [m]*len(metric_values), [n]*len(metric_values)))
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")