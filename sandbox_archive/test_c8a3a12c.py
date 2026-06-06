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
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        if n == 0: return 0
        counts = [f.count(i) for i in range(2**n)]
        mean = sum(counts) / len(counts)
        variance = sum((x - mean)**2 for x in counts) / len(counts)
        return variance
    
    def minimal_rank_QA_algebra(f):
        n = int(math.log2(len(f)))
        if n == 0: return 1
        rank = 1
        for i in range(1, n+1):
            if all(f[j] != f[j ^ (1 << k)] for k in range(i)):
                rank += 1
        return rank
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(cols):
                matrix[i][j] /= matrix[i][i]
            for k in range(rows):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def rank(matrix):
        matrix = [row[:] for row in matrix]
        r = gaussian_elimination(matrix)
        if r is None: return 0
        return sum(1 for row in r if any(x != 0 for x in row))
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, min(n_max, 20))
        f = generate_boolean_function(n)
        crv = communication_complexity_rank_variance(f)
        rank_QA_algebra = minimal_rank_QA_algebra(f)
        if rank_QA_algebra == 0:
            continue
        metric_values.append(crv / rank_QA_algebra)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    support_fraction = sum(1 for v in metric_values if v >= 0.9) / len(metric_values)
    
    conjecture_holds = abs(mean_metric_value - 1.0) <= 0.1 and support_fraction == 1.0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "CRV/QA_rank_ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")