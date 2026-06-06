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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_rank(A):
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank

    def variance_ratio(matrix):
        n = len(matrix)
        mean = sum(sum(row) for row in matrix) / (n * n)
        var = sum((x - mean) ** 2 for row in matrix for x in row) / (n * n)
        return var / n if var != 0 else float('inf')

    def formal_context(instance):
        n = len(instance)
        FC = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if instance[i][j]:
                    FC[i][j] = 1
                    FC[j][i] = 1
        return FC

    def communication_complexity_instance(n):
        instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            instance[i][i] = 0
        return instance

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = communication_complexity_instance(n)
        FC = formal_context(instance)
        rank = matrix_rank(FC)
        var_ratio = variance_ratio(instance)
        
        if var_ratio == float('inf'):
            continue
        
        metric_values.append(rank / var_ratio)

    mean_value = sum(metric_values) / len(metric_values)
    conjecture_holds = 0.5 <= mean_value <= 2
    counterexample = "" if conjecture_holds else f"Mean value: {mean_value}"
    
    return {
        "metric_name": "Minimal Order of Formal Contexts and Variance Ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results)} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")