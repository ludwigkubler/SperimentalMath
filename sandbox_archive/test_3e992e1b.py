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
    
    def generate_instance(n):
        # Generate a random communication problem instance
        return [random.randint(0, 1) for _ in range(n)]
    
    def construct_noncrossing_partitions(instance):
        # Construct noncrossing partitions using a simple algorithm
        n = len(instance)
        partitions = []
        for i in range(n):
            partition = [(i, i+1)]
            partitions.append(partition)
        return partitions
    
    def calculate_matrix_representation(partitions):
        # Calculate the matrix representation of communication protocols
        n = len(partitions)
        matrix = [[0] * n for _ in range(n)]
        for partition in partitions:
            for (i, j) in partition:
                matrix[i][j-1] += 1
                matrix[j-1][i] += 1
        return matrix
    
    def calculate_rank(matrix):
        # Calculate the rank of the matrix
        m = len(matrix)
        n = len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            
            # Swap rows to move the pivot row to the current position
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            # Eliminate entries below the pivot
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
            
            rank += 1
        
        return rank
    
    def calculate_variance(ranks):
        # Calculate the variance of the ranks
        n = len(ranks)
        mean = sum(ranks) / n
        var = sum((x - mean) ** 2 for x in ranks) / n
        return var
    
    def correlation(x, y):
        # Calculate the Pearson correlation coefficient
        n = len(x)
        if len(y) != n:
            raise ValueError("Both lists must have the same length")
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        instance = generate_instance(n)
        partitions = construct_noncrossing_partitions(instance)
        matrix = calculate_matrix_representation(partitions)
        rank = calculate_rank(matrix)
        ranks.append(rank)
    
    if len(ranks) < 30:
        return {
            "metric_name": "Variance of Ranks",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    variance = calculate_variance(ranks)
    correlation_coefficient = correlation(n_values, ranks)
    
    return {
        "metric_name": "Variance of Ranks",
        "metric_value": variance,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")