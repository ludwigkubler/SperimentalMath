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
    
    def generate_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1)**j * matrix[0][j] * determinant(submatrix)
        return det
    
    def communication_complexity(matrix):
        n = len(matrix)
        total = 0
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    total += math.log2(1 / (1 + determinant([[matrix[i][k] for k in range(j)] for k in range(i+1, n)])))
        return total
    
    def entanglement_entropy(matrix):
        n = len(matrix)
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        return -2 * math.log2(abs(det))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        matrix = generate_matrix(n)
        H_E = entanglement_entropy(matrix)
        if H_E > math.log2(n):
            continue
        CC_D = communication_complexity(matrix)
        results.append((n, H_E, CC_D))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    mean_CC_D = sum(CC_D for _, _, CC_D in results) / len(results)
    std_CC_D = math.sqrt(sum((CC_D - mean_CC_D)**2 for _, _, CC_D in results) / len(results))
    conjecture_holds = all(CC_D <= H_E**2 * math.log2(n)**2 for n, H_E, CC_D in results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_CC_D,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")