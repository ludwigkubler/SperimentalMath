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

def generate_disjointness_instance(n):
    instance = []
    for i in range(1, 2**n):
        subset = [j for j in range(n) if (i & (1 << j)) != 0]
        instance.append(subset)
    return instance

def incidence_matrix(instance):
    n = len(instance)
    m = len(instance[0])
    matrix = [[0] * m for _ in range(m)]
    for i, subset in enumerate(instance):
        for j, other_subset in enumerate(instance):
            if all(x in subset for x in other_subset):
                matrix[i][j] = 1
    return matrix

def noncrossing_partition(matrix):
    n = len(matrix)
    partition = []
    for i in range(n):
        for j in range(i+1, n):
            if all(matrix[i][j & (1 << k)] == matrix[j // (2**(i+1))][j % (2**(i+1))] for k in range(i)):
                partition.append((i, j))
    return partition

def min_rank(matrix):
    m = len(matrix)
    rank = 0
    for i in range(m):
        if any(matrix[j][i] != 0 for j in range(rank)):
            rank += 1
            for j in range(m):
                if matrix[j][i] != 0:
                    for k in range(i):
                        matrix[j][k] -= (matrix[j][i] * matrix[i][k]) / matrix[i][i]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        instance = generate_disjointness_instance(n)
        matrix = incidence_matrix(instance)
        partition = noncrossing_partition(matrix)
        rank = min_rank(matrix)
        metric_values.append(rank)
    
    mean_value = sum(metric_values) / len(metric_values)
    support_fraction = sum(1 for v in metric_values if v >= n * 3 / 2) / len(n_values)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else f"rank={max(metric_values)}, expected={n_values[-1] * 3 / 2}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")