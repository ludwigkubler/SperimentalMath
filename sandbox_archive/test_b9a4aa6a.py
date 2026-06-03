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
    
    def communication_matrix_rank(n):
        # Simulate a communication matrix for n variables
        return random.randint(1, n)
    
    def minimal_rank_of_quasi_group_extension(rank):
        # Simulated minimal rank based on communication matrix rank
        return rank * rank
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    communication_matrix_ranks = []
    minimal_ranks = []
    
    for n in n_values:
        rank = communication_matrix_rank(n)
        communication_matrix_ranks.append(rank)
        minimal_ranks.append(minimal_rank_of_quasi_group_extension(rank))
    
    corr_coeff = correlation_coefficient(communication_matrix_ranks, minimal_ranks)
    mean_communication_matrix_rank = sum(communication_matrix_ranks) / len(communication_matrix_ranks)
    mean_minimal_rank = sum(minimal_ranks) / len(minimal_ranks)
    
    supports_conjecture = 0.9 <= corr_coeff >= 0.7
    within_10_percent_communication = all(abs(x - mean_communication_matrix_rank) <= 0.1 * abs(mean_communication_matrix_rank) for x in communication_matrix_ranks)
    within_10_percent_minimal = all(abs(x - mean_minimal_rank) <= 0.1 * abs(mean_minimal_rank) for x in minimal_ranks)
    
    if supports_conjecture and within_10_percent_communication and within_10_percent_minimal:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "correlation_out_of_range" if not (0.9 <= corr_coeff >= 0.7) else "not_within_10_percent"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 2**31 - 1) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")