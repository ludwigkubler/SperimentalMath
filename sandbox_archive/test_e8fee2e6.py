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
    
    def generate_boolean_algebra(n):
        return [tuple(random.choice([0, 1]) for _ in range(n)) for _ in range(2**n)]
    
    def geometric_quantization_matrix(boolean_algebra):
        n = len(boolean_algebra[0])
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if all(x == y for x, y in zip(boolean_algebra[i], boolean_algebra[j])):
                    matrix[i][j] = 1
        return matrix
    
    def communication_protocol_efficiency(n):
        # Simplified model: O(log(n)) bits
        return math.log(n, 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_algebra = generate_boolean_algebra(n)
        matrix = geometric_quantization_matrix(boolean_algebra)
        rank = sum(1 for row in matrix if any(row))
        efficiency = communication_protocol_efficiency(n)
        results.append({"n": n, "rank": rank, "efficiency": efficiency})
    
    correlation_coefficient = 0
    if len(results) > 1:
        x_mean = sum(result["rank"] for result in results) / len(results)
        y_mean = sum(result["efficiency"] for result in results) / len(results)
        numerator = sum((result["rank"] - x_mean) * (result["efficiency"] - y_mean) for result in results)
        denominator = math.sqrt(sum((result["rank"] - x_mean)**2 for result in results)) * math.sqrt(sum((result["efficiency"] - y_mean)**2 for result in results))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "low_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")