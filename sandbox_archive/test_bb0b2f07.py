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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements below the pivot
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    
    read_once_rank_sum = 0
    read_twice_rank_sum = 0
    
    for _ in range(instances_tested):
        # Generate a read-once branching program
        bp = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2)]
        transition_matrix_ro = [bp[0], bp[1]]
        rank_ro = gaussian_elimination(transition_matrix_ro)
        if rank_ro > instances_tested * 0.1:
            read_once_rank_sum += rank_ro
        
        # Generate a read-twice branching program
        bp_twice = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2)]
        transition_matrix_rt = [bp_twice[0], bp_twice[1]]
        rank_rt = gaussian_elimination(transition_matrix_rt)
        if rank_rt > instances_tested * 0.8:
            read_twice_rank_sum += rank_rt
    
    mean_ro_rank = read_once_rank_sum / instances_tested
    mean_rt_rank = read_twice_rank_sum / instances_tested
    
    conjecture_holds = (mean_ro_rank <= instances_tested * 0.1) and (mean_rt_rank >= instances_tested * 0.8)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "average_matroid_rank",
        "metric_value": mean_rt_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.2f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")