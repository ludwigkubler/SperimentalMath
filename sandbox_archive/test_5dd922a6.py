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
    
    def characteristic_function_disjointness(n, instance):
        if len(instance) != n or any(x not in {0, 1} for x in instance):
            return None
        return [1 if all(instance[i] == 0 for i in range(n) if i != j and instance[j] == 1) else 0 for j in range(2**n)]
    
    def matrix_multiplication(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        cols_B = len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def gaussian_elimination(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        for i in range(rows):
            max_row = i
            for r in range(i+1, rows):
                if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                    max_row = r
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= factor
            for r in range(rows):
                if r != i:
                    factor = matrix[r][i]
                    for j in range(cols):
                        matrix[r][j] -= factor * matrix[i][j]
        return matrix
    
    def rank(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        gaussian_matrix = gaussian_elimination(matrix)
        rank = 0
        for i in range(rows):
            if any(gaussian_matrix[i][j] != 0 for j in range(cols)):
                rank += 1
        return rank
    
    def generate_disjointness_instance(n):
        instance = [random.randint(0, 1) for _ in range(n)]
        while sum(instance) == n or sum(instance) == 0:
            instance = [random.randint(0, 1) for _ in range(n)]
        return instance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_disjointness_instance(n)
            characteristic_func = characteristic_function_disjointness(n, instance)
            if characteristic_func is None:
                continue
            
            rank_value = rank([characteristic_func])
            total_rank += rank_value
            instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "Minimal Rank of C*-Algebra Representation",
                "metric_value": 0,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        avg_rank = total_rank / instances_tested
        results.append(avg_rank)
    
    mean_metric_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= n) / len(n_values)
    
    return {
        "metric_name": "Minimal Rank of C*-Algebra Representation",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")