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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        if matrix[max_row][i] == 0:
            continue
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if j != i:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def construct_tropicalized_config_space(T):
    # Placeholder function to simulate the construction of the tropicalized config space
    # This is a dummy implementation and should be replaced with actual logic
    n, m = len(T[0]), len(T)
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(1, n // 2)
    
    T1 = [[random.choice([0, 1]) for _ in range(n // 2)] for _ in range(m)]
    T2 = [[random.choice([0, 1]) for _ in range(n // 2)] for _ in range(m)]
    T = [T1, T2]
    
    rank = construct_tropicalized_config_space(T)
    lower_bound = n * (n / m)  # Simplified lower bound for demonstration purposes
    
    return {
        "metric_name": "Rank vs DPLL Height",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= lower_bound - 3 * math.sqrt(lower_bound),
        "counterexample": "" if rank >= lower_bound - 3 * math.sqrt(lower_bound) else f"Rank {rank} < {lower_bound - 3 * math.sqrt(lower_bound)}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")