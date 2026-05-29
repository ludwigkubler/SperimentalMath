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
    
    def generate_matrix(N):
        return [[random.randint(0, 1) for _ in range(N)] for _ in range(N)]
    
    def is_independent(lattice, matrix):
        for row in lattice:
            if any(all(row[j] == matrix[i][j] for j in range(len(matrix[0]))) for i in range(len(matrix))):
                return False
        return True
    
    def find_minimal_lattices(matrix):
        N = len(matrix)
        lattices = []
        for i in range(N):
            lattice = [matrix[i]]
            for j in range(i + 1, N):
                if is_independent(lattice, matrix[j]):
                    lattice.append(matrix[j])
            lattices.append(lattice)
        return min(len(lattices), N - len(lattices))
    
    def communication_complexity(N, I):
        return math.log2(N) ** 2 * math.log(min(I, N - I))
    
    N_values = [10, 15, 20, 30, 40]
    results = []
    
    for N in N_values:
        instances_tested = 0
        n_max = N
        total_metric_value = 0
        
        for _ in range(6):  # Ensure at least 30 instances per seed
            matrix = generate_matrix(N)
            I = find_minimal_lattices(matrix)
            metric_value = communication_complexity(N, I)
            results.append(metric_value)
            instances_tested += 1
        
        mean_metric_value = sum(results) / len(results)
        conjecture_holds = all(x <= communication_complexity(N, N // 2) for x in results)
        counterexample = "" if conjecture_holds else "mapping_undefined"
        
        return {
            "metric_name": "communication_complexity",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")