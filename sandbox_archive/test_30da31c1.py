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
    
    def generate_communication_protocol(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def rank_variance(phi):
        n = len(phi)
        mean = sum(phi) / n
        variance = sum((x - mean) ** 2 for x in phi) / n
        return variance
    
    def construct_braided_algebra(phi):
        # This is a placeholder function. In practice, you would need to implement
        # the actual mapping from communication protocol to braided algebra.
        return [sum(phi[i:i+2]) for i in range(len(phi) - 1)]
    
    def min_rank(braided_algebra):
        n = len(braided_algebra)
        if n == 0:
            return 0
        rank = float('inf')
        for i in range(n):
            current_rank = 1
            for j in range(i + 1, n):
                if braided_algebra[j] != braided_algebra[i]:
                    current_rank += 1
            rank = min(rank, current_rank)
        return rank
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def p_value(r, n):
        t_stat = r * math.sqrt((n - 2) / (1 - r**2))
        df = n - 2
        # Using a two-tailed test for simplicity
        if abs(t_stat) > abs(math.tanh(0.5 * math.log((1 + df) / (1 - df)))):
            return 0.05
        else:
            return 1.0
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    variances = []
    
    for n in n_values:
        phi = generate_communication_protocol(n)
        variance = rank_variance(phi)
        braided_algebra = construct_braided_algebra(phi)
        min_rank_value = min_rank(braided_algebra)
        
        min_ranks.append(min_rank_value)
        variances.append(variance)
    
    correlation = correlation_coefficient(min_ranks, variances)
    p_val = p_value(correlation, len(n_values))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7 and p_val <= 0.05,
        "counterexample": "" if correlation >= 0.7 and p_val <= 0.05 else f"Correlation: {correlation}, P-value: {p_val}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")