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
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot row
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = 0
    for i in range(n):
        if any(matrix[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate a read-once branching program
    transition_matrix_ro = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    rank_ro = gaussian_elimination(transition_matrix_ro)
    
    # Generate a read-twice branching program
    transition_matrix_rw = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    rank_rw = gaussian_elimination(transition_matrix_rw)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value_ro": rank_ro,
        "metric_value_rw": rank_rw,
        "instances_tested": 1,
        "conjecture_holds_ro": rank_ro <= 0.1 * n,
        "counterexample_ro": "" if rank_ro <= 0.1 * n else f"Read-once BP with rank {rank_ro}",
        "conjecture_holds_rw": rank_rw >= 0.8 * n,
        "counterexample_rw": "" if rank_rw >= 0.8 * n else f"Read-twice BP with rank {rank_rw}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results_ro = []
    results_rw = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds_ro"]:
            return f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample_ro']}\" first_failing_seed={seed}"
        results_ro.append(trial_result["metric_value_ro"])
        
        if not trial_result["conjecture_holds_rw"]:
            return f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample_rw']}\" first_failing_seed={seed}"
        results_rw.append(trial_result["metric_value_rw"])
    
    mean_ro = sum(results_ro) / len(results_ro)
    std_ro = math.sqrt(sum((x - mean_ro) ** 2 for x in results_ro) / len(results_ro))
    support_fraction_ro = len([x for x in results_ro if x >= 0.1 * n]) / len(results_ro)
    
    mean_rw = sum(results_rw) / len(results_rw)
    std_rw = math.sqrt(sum((x - mean_rw) ** 2 for x in results_rw) / len(results_rw))
    support_fraction_rw = len([x for x in results_rw if x >= 0.8 * n]) / len(results_rw)
    
    return f"RESULT: SUPPORTED mean_ro={mean_ro} std_ro={std_ro} support_fraction_ro={support_fraction_ro} mean_rw={mean_rw} std_rw={std_rw} support_fraction_rw={support_fraction_rw}"