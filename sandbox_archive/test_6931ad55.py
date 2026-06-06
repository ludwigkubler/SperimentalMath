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
    
    def generate_boolean_function(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        return f
    
    def noncrossing_partitions(matrix):
        n = len(matrix)
        if n == 1:
            return 1
        partitions = [0] * (n + 1)
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                j = i + k
                partitions[j] += partitions[i] * partitions[j - i - 1]
        return partitions[n]
    
    def rank_variance(matrix):
        n = len(matrix)
        mean = sum(sum(row) for row in matrix) / (n * n)
        variance = sum((sum(row) - mean)**2 for row in matrix) / (n * n)
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        matrix = matrix_representation(f)
        partitions_order = noncrossing_partitions(matrix)
        rank_var = rank_variance(matrix)
        results.append({
            "n": n,
            "partitions_order": partitions_order,
            "rank_var": rank_var
        })
    
    mean_partitions_order = sum(result["partitions_order"] for result in results) / len(results)
    std_partitions_order = math.sqrt(sum((result["partitions_order"] - mean_partitions_order)**2 for result in results) / len(results))
    mean_rank_var = sum(result["rank_var"] for result in results) / len(results)
    std_rank_var = math.sqrt(sum((result["rank_var"] - mean_rank_var)**2 for result in results) / len(results))
    
    conjecture_holds = all(mean_partitions_order <= 1.5 * std_partitions_order + mean_rank_var for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Noncrossing Partitions Order",
        "metric_value": mean_partitions_order,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")