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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(-A[i][i], A[i][i])
            for j in range(n):
                if i != j:
                    A[j][i] += factor * A[i][j]
        return A
    
    def characteristic_polynomial(f, n):
        A = [[0] * (n+1) for _ in range(n+1)]
        for i in range(n):
            for j in range(i+1):
                if f(j) == 1:
                    A[j][i] += 1
        return gaussian_elimination(A)
    
    def geometric_entropy(poly):
        # Placeholder for actual computation of geometric entropy
        # This is a dummy implementation for testing purposes
        return sum(abs(coeff) for coeff in poly[-1])
    
    def communication_complexity_rank_variance(f, n):
        # Placeholder for actual computation of communication complexity rank variance
        # This is a dummy implementation for testing purposes
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        f = lambda x: random.choice([0, 1])  # Random Boolean function
        poly = characteristic_polynomial(f, n)
        ge = geometric_entropy(poly)
        rcv = communication_complexity_rank_variance(f, n)
        metrics.append((ge, rcv))
    
    if len(metrics) < 30:
        return {
            "metric_name": "GE vs RCV",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ge_values = [ge for ge, _ in metrics]
    rcv_values = [rcv for _, rcv in metrics]
    correlation_coefficient = sum((ge - mean_ge) * (rcv - mean_rcv) for ge, rcv in zip(ge_values, rcv_values)) / len(metrics)
    mean_ge = sum(ge_values) / len(ge_values)
    mean_rcv = sum(rcv_values) / len(rcv_values)
    
    return {
        "metric_name": "GE vs RCV",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.1,  # Arbitrary threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")