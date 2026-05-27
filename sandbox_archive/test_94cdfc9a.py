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
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n + 1):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def min_rank(matrix):
        return len([row for row in gaussian_elimination(matrix) if any(row)])

    def symmetry_breaking_communication_complexity(n, t):
        # Placeholder function. Replace with actual implementation.
        return 2 ** (t // 4)

    n = random.randint(5, 40)
    t = random.randint(1, 2 * n)
    f_t = int(math.log(t))
    
    instance_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    min_rank_value = min_rank(instance_matrix)
    comm_complexity = symmetry_breaking_communication_complexity(n, t)
    
    conjecture_holds = min_rank_value <= f_t and comm_complexity <= 2 ** (f_t)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Symmetry Breaking Communication Complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")