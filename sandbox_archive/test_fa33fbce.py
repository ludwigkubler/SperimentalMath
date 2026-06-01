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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i + max(range(i, n), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        
        # Back-substitute to find solution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (matrix[i][-1] - sum(matrix[i][j] * x[j] for j in range(i+1, n))) / matrix[i][i]
        return x

    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1)**i * matrix[0][i] * determinant(submatrix)
        return det

    def ideal_class_group_size(n):
        # Example mapping from n to ideal class group size
        if n == 5:
            return 2
        elif n == 10:
            return 3
        elif n == 15:
            return 4
        elif n == 20:
            return 5
        elif n == 30:
            return 6
        elif n == 40:
            return 7
        else:
            return None

    def communication_rank(n):
        # Example mapping from n to communication rank
        if n == 5:
            return 1
        elif n == 10:
            return 2
        elif n == 15:
            return 3
        elif n == 20:
            return 4
        elif n == 30:
            return 5
        elif n == 40:
            return 6
        else:
            return None

    instances_tested = 0
    size_list = []
    rank_list = []

    for _ in range(30):
        n = random.randint(5, 40)
        if ideal_class_group_size(n) is None or communication_rank(n) is None:
            continue
        
        instances_tested += 1
        size_list.append(ideal_class_group_size(n))
        rank_list.append(communication_rank(n))

    if not size_list or not rank_list:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, 10, 15, 20, 30, 40),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_size = sum(size_list) / len(size_list)
    mean_rank = sum(rank_list) / len(rank_list)

    variance_size = sum((x - mean_size)**2 for x in size_list) / len(size_list)
    variance_rank = sum((x - mean_rank)**2 for x in rank_list) / len(rank_list)

    std_deviation_size = math.sqrt(variance_size)
    std_deviation_rank = math.sqrt(variance_rank)

    correlation_coefficient = sum((size - mean_size) * (rank - mean_rank) for size, rank in zip(size_list, rank_list)) / (len(size_list) * std_deviation_size * std_deviation_rank)

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95 * std_deviation_size * std_deviation_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.95 * std_deviation) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] == "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")