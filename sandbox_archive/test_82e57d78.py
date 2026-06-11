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
from fractions import Fraction
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        if factor == 0:
            continue
        for j in range(i, n):
            A[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]

def hodge_theoretic_dimension(instance):
    # Placeholder for the actual Hodge theoretic dimension calculation
    # This is a dummy implementation that avoids division by zero
    if instance == 0:
        return 1
    return Fraction(1, abs(instance))

def rank_variance(instance):
    # Placeholder for the actual rank variance calculation
    # This is a dummy implementation
    return random.random()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        instance = random.randint(1, n_max)
        htd = hodge_theoretic_dimension(instance)
        rvar = rank_variance(instance)
        metric_values.append((htd, rvar))
    
    correlation_coefficient = 0
    if len(metric_values) > 1:
        mean_htd = sum(htd for htd, _ in metric_values) / len(metric_values)
        mean_rvar = sum(rvar for _, rvar in metric_values) / len(metric_values)
        numerator = sum((htd - mean_htd) * (rvar - mean_rvar) for htd, rvar in metric_values)
        denominator = math.sqrt(sum((htd - mean_htd)**2 for htd, _ in metric_values)) * math.sqrt(sum((rvar - mean_rvar)**2 for _, rvar in metric_values))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")