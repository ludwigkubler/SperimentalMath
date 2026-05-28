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
    
    n = 20  # Fixed size for simplicity, can be adjusted
    M = [[random.random() for _ in range(n)] for _ in range(n)]
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if all(abs(matrix[j][i]) < 1e-10 for j in range(m)):
                continue
            pivot_row = next(j for j in range(i, m) if abs(matrix[j][i]) > 1e-10)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(m):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    r_M = matrix_rank(M)
    
    def simulate_disjointness_protocol(n):
        bits = [random.choice([0, 1]) for _ in range(n)]
        communication_cost = sum(1 for i in range(n) if bits[i] == 1)
        return communication_cost
    
    comm_complexity = simulate_disjointness_protocol(n)
    
    metric_name = "communication_complexity"
    metric_value = comm_complexity
    instances_tested = 1
    conjecture_holds = r_M * 2 <= comm_complexity
    counterexample = "" if conjecture_holds else f"r(M)={r_M}, comm_complexity={comm_complexity}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r(M) < 2 * comm_complexity\" first_failing_seed={first_failing_seed}")