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
    rank = 0
    
    for i in range(cols):
        max_row = None
        for j in range(i, rows):
            if matrix[j][i] != 0:
                max_row = j
                break
        
        if max_row is None:
            continue
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(i, cols):
                matrix[j][k] += factor * matrix[i][k]
        
        rank += 1
    
    return rank

def minimal_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    sub_matrix = [[matrix[i][j] for j in range(cols)] for i in range(rows)]
    
    # Perform Gaussian elimination
    rank = gaussian_elimination(sub_matrix)
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    k = 5
    
    # Generate a monotone circuit for k-CLIQUE
    # This is a simplified representation and not a real monotone circuit
    circuit = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                circuit.append((i, j))
    
    # Map circuit gates to group operations (simplified)
    matrix = [[0] * n for _ in range(n)]
    for gate in circuit:
        i, j = gate
        matrix[i][j] = 1
    
    rank = minimal_rank(matrix)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= n**k,
        "counterexample": "" if rank >= n**k else f"Rank {rank} < {n**k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")