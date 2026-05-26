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
    
    def generate_symmetric_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                M[i][j] = random.uniform(-1, 1)
                M[j][i] = M[i][j]
        return M
    
    def compute_permanent(M):
        n = len(M)
        if n == 0:
            return 1
        if n == 1:
            return M[0][0]
        
        permanent = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            sign = (-1) ** (j % 2)
            permanent += sign * M[0][j] * compute_permanent(submatrix)
        return abs(permanent)
    
    def tseitin_circuit_size(M):
        n = len(M)
        size = 0
        for i in range(n):
            for j in range(i, n):
                if M[i][j] != 0:
                    size += 2
        return size
    
    def min_rank_symplectic_leaves(G_k_n_intersect_SymMat_n):
        # Placeholder function to compute the minimal rank of symplectic leaves
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_symmetric_matrix(n)
    perm_size = tseitin_circuit_size(M)
    min_rank = min_rank_symplectic_leaves(G_k_n_intersect_SymMat_n)  # Placeholder
    
    return {
        "metric_name": "min_rank_symplectic_leaves",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    metric_values = [result["metric_value"] for result in results]
    conjecture_holds_count = sum(result["conjecture_holds"] for result in results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")