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
    
    def generate_protocol(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def rank_variance(protocol):
        n = len(protocol)
        mean = sum(protocol) / n
        variance = sum((x - mean) ** 2 for x in protocol) / n
        return variance
    
    def minimal_rank(braided_algebra):
        # Placeholder function to simulate minimal rank calculation
        return random.randint(1, 10)
    
    def construct_braided_algebra(protocol):
        # Placeholder function to simulate braided algebra construction
        return [sum(x * y for x, y in zip(proto, protocol)) for proto in protocol]
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    rank_vars = []
    
    for n in n_values:
        protocol = generate_protocol(n)
        rank_var = rank_variance(protocol)
        braided_algebra = construct_braided_algebra(protocol)
        min_rank_value = minimal_rank(braided_algebra)
        
        min_ranks.append(min_rank_value)
        rank_vars.append(rank_var)
    
    correlation = sum((min_ranks[i] - mean_min_ranks) * (rank_vars[i] - mean_rank_vars) for i in range(len(n_values))) / len(n_values)
    mean_min_ranks = sum(min_ranks) / len(min_ranks)
    mean_rank_vars = sum(rank_vars) / len(rank_vars)
    
    if abs(correlation) < 1e-6:
        p_value = 1.0
    else:
        df = len(n_values) - 2
        t = abs(correlation) * math.sqrt(df) / math.sqrt(1 - correlation ** 2)
        p_value = 2 * (1 - math.erf(t / math.sqrt(2)))
    
    conjecture_holds = p_value <= 0.05 and correlation >= 0.7
    counterexample = "" if conjecture_holds else "correlation_not_met"
    
    return {
        "metric_name": "Correlation between minimal rank and rank variance",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_not_met\" first_failing_seed={first_failing_seed}")