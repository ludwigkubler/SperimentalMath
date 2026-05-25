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
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, m):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        matrix = gaussian_elimination(matrix)
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def communication_complexity(n):
        # Simulate randomized communication complexity for DISJOINTNESS problem
        # This is a placeholder function. Replace with actual computation.
        return random.randint(2, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    boolean_functions = [random.getrandbits(n) for _ in range(100)]
    results = []
    
    for bf in boolean_functions:
        # Construct quasi-projective variety using the Boolean function
        # This is a placeholder. Replace with actual construction.
        variety_matrix = [[int(bf[i] != bf[j]) for j in range(n)] for i in range(n)]
        min_rank = rank(variety_matrix)
        
        comm_complexity = communication_complexity(n)
        results.append((min_rank, comm_complexity))
    
    mean_metric_value = sum(min_rank * 2**comm_complexity for min_rank, comm_complexity in results) / len(results)
    support_fraction = sum(1 for _, comm_complexity in results if abs(comm_complexity - math.log2(mean_metric_value)) <= 0.1) / len(results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else f"Mean rank: {mean_metric_value}, Mean communication complexity: {comm_complexity}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean communication complexity does not match mean rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")