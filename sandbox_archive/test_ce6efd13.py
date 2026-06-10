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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        inputs = [i for i in range(2**n)]
        ranks = []
        for input_val in inputs:
            binary_input = f"{input_val:0{n}b}"
            rank = 1
            for i in range(n):
                if binary_input[i] == '1':
                    rank *= (i + 1)
            ranks.append(rank)
        return sum(ranks) / len(ranks)
    
    def p_adic_derivative_rank(f):
        n = len(f)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if f[i] != f[j]:
                    A[i][j] = 1
                    A[j][i] = 1
        rank = 0
        for row in A:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(i + 1, n):
                            if A[i][j]:
                                A[j][i] = 0
        return rank
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) * sum((y[i] - mean_y)**2 for i in range(n)))
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    mdr_values = []
    delta_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        delta = communication_complexity_rank_variance(f)
        mdr = p_adic_derivative_rank(f)
        mdr_values.append(mdr)
        delta_values.append(delta)
    
    correlation_coefficient = pearson_correlation_coefficient(mdr_values, delta_values)
    conjecture_holds = 0.6 <= correlation_coefficient >= 0.8 and all(mdr <= 1.2 * delta for mdr, delta in zip(mdr_values, delta_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(res["mdr"] > 1.5 * res["delta"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if res["mdr"] > 1.5 * res["delta"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")