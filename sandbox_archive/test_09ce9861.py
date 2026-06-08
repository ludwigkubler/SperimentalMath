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

def generate_matrix(n):
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return matrix

def matrix_multiplication(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix)
    return det

def characteristic_polynomial(matrix):
    n = len(matrix)
    char_poly = [1]
    for i in range(n):
        char_poly.append(-sum(char_poly[-2::-1]))
    return char_poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        matrix = generate_matrix(n)
        rank = sum(1 for row in matrix if any(row))
        char_poly = characteristic_polynomial(matrix)
        min_local_index = len(char_poly)
        results.append((n, rank, min_local_index))
    
    log_msl = [math.log(msl) for _, _, msl in results]
    var_rank = sum((r - sum(ranks) / len(ranks)) ** 2 for _, r, _ in results) / len(results)
    correlation_coefficient = sum((log_msl[i] - mean_log_msl) * (var_rank[i] - mean_var_rank) for i in range(len(log_msl))) / (len(log_msl) * math.sqrt(sum((log_msl[i] - mean_log_msl) ** 2 for i in range(len(log_msl)))) * math.sqrt(sum((var_rank[i] - mean_var_rank) ** 2 for i in range(len(var_rank)))))
    
    mean_log_msl = sum(log_msl) / len(log_msl)
    mean_var_rank = sum(var_rank) / len(var_rank)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r) >= 0.7) / len(results)
    
    if all(abs(r) >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if abs(r) < 0.7)]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_sufficiently_high\" first_failing_seed={first_failing_seed}")