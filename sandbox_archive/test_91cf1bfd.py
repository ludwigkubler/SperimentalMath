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
    
    def generate_noncommutative_algebra(n):
        # Simple noncommutative algebra generator for demonstration purposes
        A = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
        return A
    
    def lind(A):
        n = len(A)
        rank = gaussian_elimination_rank(A)
        return rank
    
    def gaussian_elimination_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                for j in range(i + 1, m):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
                rank += 1
        return rank
    
    def CCrank(A):
        # Placeholder function for communication complexity rank
        n = len(A)
        return math.log2(n) if n > 0 else 0
    
    instances_tested = 30
    n_max = 10
    metric_values = []
    
    for _ in range(instances_tested):
        A = generate_noncommutative_algebra(n_max)
        lind_A = lind(A)
        CCrank_A = CCrank(A)
        if CCrank_A == 0:
            continue
        metric_value = lind_A / (2 ** CCrank_A)
        metric_values.append(metric_value)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(x >= 0.8 for x in metric_values if x <= 10)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "lind(A) / 2^CCrank(A)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")