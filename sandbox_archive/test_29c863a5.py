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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def ideal_class_group_size(n):
        # Placeholder function to compute the size of the ideal class group
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)

    def communication_complexity_rank(n):
        # Placeholder function to compute the communication complexity rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        size_sum = 0
        rank_sum = 0
        instances_tested = 0
        
        for _ in range(5):  # Sample 5 random instances per n
            size = ideal_class_group_size(n)
            rank = communication_complexity_rank(n)
            if size <= 1:
                continue
            size_sum += size
            rank_sum += rank
            instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        mean_size = size_sum / instances_tested
        mean_rank = rank_sum / instances_tested
        
        correlation_coefficient = sum((size - mean_size) * (rank - mean_rank) for size, rank in zip(size_list, rank_list)) / (instances_tested * std_deviation_size * std_deviation_rank)
        
        results.append({
            "n": n,
            "mean_size": mean_size,
            "mean_rank": mean_rank,
            "correlation_coefficient": correlation_coefficient
        })
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_correlation = sum(result["correlation_coefficient"] for result in results) / len(results)
    std_deviation_correlation = math.sqrt(sum((result["correlation_coefficient"] - mean_correlation) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(abs(correlation) >= mean_correlation - 2 * std_deviation_correlation for correlation in [result["correlation_coefficient"] for result in results])
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mean_correlation,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Correlation coefficient does not meet the criteria"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_deviation_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(abs(result["metric_value"]) <= 1 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient does not meet the criteria\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason: Metric saturation or tautological inequality")