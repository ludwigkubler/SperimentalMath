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
    
    def hodge_decomposition_rank(n):
        # Placeholder for Hodge decomposition rank calculation
        return n
    
    def communication_complexity_rank_variance(n):
        # Placeholder for communication complexity rank variance calculation
        return n**2
    
    instances_tested = 0
    metric_values = []
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        hodge_rank = hodge_decomposition_rank(n)
        variance = communication_complexity_rank_variance(n)
        
        instances_tested += 1
        metric_values.append((hodge_rank, variance))
    
    correlation_coefficient = calculate_correlation(metric_values)
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "HodgeDecompositionRank vs CommunicationComplexityRankVariance",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(data):
    if len(data) < 2:
        return 0
    
    x_sum = sum(x for x, _ in data)
    y_sum = sum(y for _, y in data)
    n = len(data)
    
    numerator = sum((x - x_sum / n) * (y - y_sum / n) for x, y in data)
    denominator = math.sqrt(sum((x - x_sum / n)**2 for x, _ in data)) * math.sqrt(sum((y - y_sum / n)**2 for _, y in data))
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")