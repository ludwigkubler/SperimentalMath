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
    
    def generate_algebra(n):
        # Generate a random noncommutative algebra with n generators
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A
    
    def lind(A):
        # Compute the minimal local indeterminacy of the algebra
        n = len(A)
        max_det = 0
        for i in range(n):
            det = 1
            for j in range(n):
                if j != i:
                    det *= abs(A[i][j])
            max_det = max(max_det, det)
        return max_det
    
    def CCrank(A):
        # Compute the communication complexity rank of the algebra
        n = len(A)
        min_rank = float('inf')
        for k in range(1, n+1):
            found = False
            for i in range(n):
                if all(A[i][j] == 0 for j in range(k, n)):
                    found = True
                    break
            if found:
                min_rank = min(min_rank, k)
        return min_rank
    
    instances_tested = 30
    n_max = 40
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        A = generate_algebra(n)
        lind_A = lind(A)
        CCrank_A = CCrank(A)
        if CCrank_A == 0:
            continue
        metric_values.append(lind_A / (2 ** CCrank_A))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(x >= 0.8 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "lind(A) / 2^CCrank(A)",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")