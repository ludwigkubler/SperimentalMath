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
    
    def generate_matrix(n: int) -> list:
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def determinant(matrix: list) -> int:
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1)**j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def euler_characteristic(matrix: list) -> int:
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] == 1 for j in range(rank)):
                rank += 1
        return n - rank
    
    def spearman_rank_correlation(x: list, y: list) -> float:
        x_ranks = {x[i]: i+1 for i in range(len(x))}
        y_ranks = {y[i]: i+1 for i in range(len(y))}
        n = len(x)
        sum_d_squared = sum((x_ranks[x[i]] - y_ranks[y[i]])**2 for i in range(n))
        return 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    
    metric_name = "communication_complexity"
    instances_tested = 0
    n_max = 0
    total_communication_complexity = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            matrix = generate_matrix(n)
            det = determinant(matrix)
            chi_M = euler_characteristic(matrix)
            communication_complexity = abs(det) + abs(chi_M)
            total_communication_complexity += communication_complexity
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_communication_complexity = total_communication_complexity / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    if instances_tested >= 30:
        # Perform Spearman rank correlation test
        communication_complexities = [abs(determinant(generate_matrix(n))) + abs(euler_characteristic(generate_matrix(n))) for n in [5, 10, 15, 20, 30, 40] for _ in range(5)]
        chi_M_values = [euler_characteristic(generate_matrix(n)) for n in [5, 10, 15, 20, 30, 40] for _ in range(5)]
        correlation_coefficient = spearman_rank_correlation(communication_complexities, chi_M_values)
        
        if correlation_coefficient >= 0.7:
            conjecture_holds = True
        else:
            counterexample = f"Spearman rank correlation coefficient {correlation_coefficient} < 0.7"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_communication_complexity,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")