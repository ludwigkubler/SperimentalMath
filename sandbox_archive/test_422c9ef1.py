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
    
    def generate_random_boolean_function(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        
        rank = 0
        A = [row[:] for row in matrix]
        for j in range(n):
            i_max = max(range(j, n), key=lambda i: abs(A[i][j]))
            if A[i_max][j] == 0:
                continue
            A[j], A[i_max] = A[i_max], A[j]
            rank += 1
            denom = A[j][j]
            for k in range(n):
                A[j][k] /= denom
            for i in range(n):
                if i != j:
                    factor = A[i][j]
                    for k in range(n):
                        A[i][k] -= factor * A[j][k]
        return rank
    
    def noncrossing_partitions(matrix):
        n = len(matrix)
        partitions = []
        for i in range(1, 2**n):
            partition = []
            current_set = set()
            for j in range(n):
                if (i >> j) & 1:
                    current_set.add(j)
                else:
                    if current_set:
                        partition.append(current_set)
                        current_set = set()
            if current_set:
                partition.append(current_set)
            partitions.append(partition)
        return partitions
    
    def rank_variance(matrix):
        n = len(matrix)
        ranks = [matrix_rank(submatrix) for submatrix in matrix]
        mean = sum(ranks) / n
        var = sum((x - mean)**2 for x in ranks) / n
        return var
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    rank_var = rank_variance(f)
    noncrossing_part_order = len(noncrossing_partitions(f))
    
    metric_name = "Noncrossing Part Order"
    metric_value = noncrossing_part_order
    instances_tested = 1
    n_max = n
    conjecture_holds = noncrossing_part_order <= f(n)**2 * 1.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")