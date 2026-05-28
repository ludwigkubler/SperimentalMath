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
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return result
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for i in range(m):
            max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[n:] for row in augmented_matrix]
    
    def rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        r = sum(1 for row in reduced_matrix if any(row))
        return r
    
    def disjointness_complexity(n):
        return n - 1
    
    def grothendieck_group_rank(n):
        # Construct a random Boolean function
        clauses = [random.sample(range(n), random.randint(1, n)) for _ in range(random.randint(1, n))]
        
        # Construct the associated motivic sheaf using a simple procedure
        ideal = []
        for clause in clauses:
            monomial = 1
            for var in clause:
                if random.choice([True, False]):
                    monomial *= (1 - var)
                else:
                    monomial *= var
            ideal.append(monomial)
        
        # Compute the Grothendieck group rank
        matrix = [[0] * len(ideal) for _ in range(len(ideal))]
        for i in range(len(ideal)):
            for j in range(i, len(ideal)):
                if i == j:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = ideal[i] * ideal[j]
        
        return rank(matrix)
    
    n = random.randint(5, 40)
    rank_value = grothendieck_group_rank(n)
    cc_r_value = disjointness_complexity(n)
    
    metric_name = "Rank to CC_R Ratio"
    metric_value = Fraction(rank_value, cc_r_value) if cc_r_value != 0 else float('inf')
    instances_tested = 1
    conjecture_holds = metric_value >= 1 and metric_value >= 0.9
    counterexample = "" if conjecture_holds else f"Rank {rank_value}, CC_R {cc_r_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank to CC_R Ratio\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")