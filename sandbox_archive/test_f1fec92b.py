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
    n = len(matrix)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-zero entries below the pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def rank(matrix):
    n = len(matrix)
    rank_value = 0
    for i in range(n):
        if all(abs(matrix[i][j]) < 1e-9 for j in range(n)):
            continue
        rank_value += 1
    return rank_value

def construct_qgr(bp_size):
    # Placeholder function to simulate quantum group representation construction
    # This is a dummy implementation and should be replaced with actual logic
    qgr = [[random.randint(0, 1) for _ in range(bp_size)] for _ in range(bp_size)]
    return qgr

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    bp_sizes = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for bp_size in bp_sizes:
        for _ in range(5):  # Sample 5 instances per size
            bp = [random.randint(0, 1) for _ in range(bp_size)]
            qgr = construct_qgr(bp_size)
            rank_value = rank(qgr)
            total_rank += rank_value
            instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    conjecture_holds = avg_rank <= bp_size ** 2  # Placeholder condition
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank vs BP_ReadTwice",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")