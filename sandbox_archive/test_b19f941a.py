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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    rank = [sum(f[i:i+n]) for i in range(2**n)]
    mean_rank = sum(rank) / len(rank)
    variance = sum((x - mean_rank)**2 for x in rank) / len(rank)
    return variance

def construct_crossed_product_algebra(f):
    n = int(math.log2(len(f)))
    algebra = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if f[i & j]:
                algebra[i][j] = 1
    return algebra

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank_variance = communication_complexity_rank_variance(f)
        if rank_variance == 0:
            continue
        crossed_product_algebra = construct_crossed_product_algebra(f)
        
        # Calculate minimal index I(n) (simplified as sum of algebra elements for demonstration purposes)
        I_n = sum(sum(row) for row in crossed_product_algebra)
        
        results.append({
            "n": n,
            "I_n": I_n,
            "rank_variance": rank_variance
        })
    
    if not results:
        return {
            "metric_name": "minimal_index",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    I_ns = [result["I_n"] for result in results]
    rank_variances = [result["rank_variance"] for result in results]
    
    # Calculate correlation coefficient
    mean_I_n = sum(I_ns) / len(I_ns)
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    numerator = sum((I_ns[i] - mean_I_n) * (rank_variances[i] - mean_rank_variance) for i in range(len(I_ns)))
    denominator = math.sqrt(sum((I_ns[i] - mean_I_n)**2 for i in range(len(I_ns)))) * math.sqrt(sum((rank_variances[i] - mean_rank_variance)**2 for i in range(len(rank_variances))))
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "minimal_index",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient > 0.8 and all(I_n / rank_variance <= 1.5 for I_n, rank_variance in zip(I_ns, rank_variances)),
        "counterexample": "" if correlation_coefficient > 0.8 else f"n={results[0]['n']}, I(n)={results[0]['I_n']}, r(n)={results[0]['rank_variance']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='{trial_result['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")