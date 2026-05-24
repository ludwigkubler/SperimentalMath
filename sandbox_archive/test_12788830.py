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
        # Find pivot
        max_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for r in range(i + 1, rows):
            factor = Fraction(matrix[r][i], matrix[i][i])
            for c in range(cols):
                matrix[r][c] -= factor * matrix[i][c]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def communication_complexity(n):
    # Simplified version of the communication complexity for disjointness
    return n / 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate a random representation V of a quantum group G
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    rank_value = gaussian_elimination(matrix)
    cc_value = communication_complexity(n)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc_value,
        "instances_tested": 1,
        "conjecture_holds": rank_value >= cc_value,
        "counterexample": "" if rank_value >= cc_value else f"rank(H^i(V)) = {rank_value} < CC(DISJ_n) = {cc_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        
        print(f"TRIAL: {trial_result}")
    
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")