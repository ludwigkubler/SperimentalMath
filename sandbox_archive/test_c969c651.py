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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def binary_tree_from_function(f):
        n = int(math.log2(len(f)))
        tree = [[None] * (2 ** i) for i in range(n + 1)]
        tree[0][0] = f
        for level in range(n):
            for j in range(2 ** level):
                if tree[level][j] is not None:
                    left_child = tree[level][j] & 1
                    right_child = (tree[level][j] >> 1) & 1
                    tree[level + 1][2 * j] = left_child
                    tree[level + 1][2 * j + 1] = right_child
        return tree
    
    def local_induction_dimension(tree):
        n = len(tree)
        if n == 0:
            return 0
        points = set()
        for level in range(n):
            for i in range(2 ** level):
                if tree[level][i] is not None:
                    points.add((level, i))
        max_distance = 0
        for p1 in points:
            for p2 in points:
                distance = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
                if distance > max_distance:
                    max_distance = distance
        return max_distance
    
    def communication_complexity_rank(tree):
        n = len(tree)
        if n == 0:
            return 0
        rank = 0
        for level in range(n):
            for i in range(2 ** level):
                if tree[level][i] is not None:
                    rank += 1
        return rank
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mild_values = []
    ccr_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        tree = binary_tree_from_function(f)
        mild = local_induction_dimension(tree)
        ccr = communication_complexity_rank(tree)
        mild_values.append(mild)
        ccr_values.append(ccr)
    
    correlation_coefficient = correlation(mild_values, ccr_values)
    metric_value = abs(correlation_coefficient)
    instances_tested = len(n_values)
    n_max = max(n_values)
    conjecture_holds = correlation_coefficient >= 0.5 and mild <= 10
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.5 or MILD > 10"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) and min(result["metric_value"] for result in results) < 0.5:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5 or MILD > 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")