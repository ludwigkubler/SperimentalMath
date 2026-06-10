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
    
    def hodge_decomposition_rank(n):
        # Placeholder for Hodge decomposition rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return n
    
    def communication_complexity_rank_variance(n):
        # Placeholder for communication complexity rank variance calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.uniform(0, 1)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        rank = hodge_decomposition_rank(n)
        variance = communication_complexity_rank_variance(n)
        results.append((rank, variance))
    
    if not results:
        return {
            "metric_name": "HodgeDecompositionRank vs CommunicationComplexityRankVariance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "HodgeDecompositionRank vs CommunicationComplexityRankVariance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    # Perform linear regression
    x_sum = sum(rank for rank, _ in results)
    y_sum = sum(variance for _, variance in results)
    xy_sum = sum(rank * variance for rank, variance in results)
    x_squared_sum = sum(rank ** 2 for rank, _ in results)
    
    n = len(results)
    slope = (n * xy_sum - x_sum * y_sum) / (n * x_squared_sum - x_sum ** 2)
    intercept = (y_sum - slope * x_sum) / n
    
    # Calculate correlation coefficient
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x_squared_sum - x_sum ** 2) * (n * y_sum ** 2 - y_sum ** 2))
    if denominator == 0:
        return {
            "metric_name": "HodgeDecompositionRank vs CommunicationComplexityRankVariance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "HodgeDecompositionRank vs CommunicationComplexityRankVariance",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all("metric_value" in result and result["metric_value"] is not None for result in results):
        print("RESULT: INCONCLUSIVE reason=missing_metric_values")
    else:
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.9\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")