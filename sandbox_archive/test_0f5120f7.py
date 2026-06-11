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
    
    def calculate_min_rank(phi):
        n = len(phi)
        entanglement_tensor = [[phi[i] if (i & j) == i else 0 for j in range(2**n)] for i in range(2**n)]
        rank = 0
        while True:
            found_non_zero_row = False
            for i in range(len(entanglement_tensor)):
                if any(row != 0 for row in entanglement_tensor[i]):
                    found_non_zero_row = True
                    break
            if not found_non_zero_row:
                break
            rank += 1
            for i in range(len(entanglement_tensor)):
                if any(row != 0 for row in entanglement_tensor[i]):
                    for j in range(len(entanglement_tensor[0])):
                        if entanglement_tensor[i][j] != 0:
                            for k in range(len(entanglement_tensor)):
                                entanglement_tensor[k][j] -= entanglement_tensor[k][i] * entanglement_tensor[i][j]
        return rank
    
    def calculate_rank_variance(phi):
        n = len(phi)
        communication_complexity_matrix = [[phi[i] if (i & j) == i else 0 for j in range(2**n)] for i in range(2**n)]
        variance = 0
        for i in range(len(communication_complexity_matrix)):
            for j in range(len(communication_complexity_matrix[0])):
                variance += communication_complexity_matrix[i][j] ** 2
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    rank_variances = []
    
    for n in n_values:
        phi = generate_boolean_function(n)
        min_rank = calculate_min_rank(phi)
        rank_variance = calculate_rank_variance(phi)
        min_ranks.append(min_rank)
        rank_variances.append(rank_variance)
    
    if len(min_ranks) < 30 or len(rank_variances) < 30:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": len(min_ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    correlation_coefficient = 0
    for i in range(len(min_ranks)):
        correlation_coefficient += (min_ranks[i] - mean_min_rank) * (rank_variances[i] - mean_rank_variance)
    correlation_coefficient /= math.sqrt(sum((x - mean_min_rank) ** 2 for x in min_ranks)) * math.sqrt(sum((y - mean_rank_variance) ** 2 for y in rank_variances))
    
    return {
        "metric_name": "min_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.8 and p_value < 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")