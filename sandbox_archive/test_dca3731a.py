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
    
    def construct_matroid(f):
        n = int(math.log2(len(f)))
        matroid = []
        for i in range(2**n):
            subset = [j for j in range(n) if (i & (1 << j))]
            if all(f[i] == f[j] for j in subset):
                matroid.append(subset)
        return matroid
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        min_bits = float('inf')
        for i in range(2**n):
            bits = 0
            for j in range(n):
                if (i & (1 << j)):
                    bits += 1
            min_bits = min(min_bits, bits)
        return min_bits
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        matroid = construct_matroid(f)
        if not matroid:
            continue
        min_rank = len(matroid)
        comm_complexity = communication_complexity(f)
        results.append({
            "n": n,
            "min_rank": min_rank,
            "comm_complexity": comm_complexity
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_matroid"
        }
    
    min_rank_values = [r["min_rank"] for r in results]
    comm_complexity_values = [r["comm_complexity"] for r in results]
    
    mean_min_rank = sum(min_rank_values) / len(min_rank_values)
    mean_comm_complexity = sum(comm_complexity_values) / len(comm_complexity_values)
    
    correlation_coefficient = 0.0
    if min_rank_values and comm_complexity_values:
        n = len(min_rank_values)
        numerator = sum((min_rank_values[i] - mean_min_rank) * (comm_complexity_values[i] - mean_comm_complexity) for i in range(n))
        denominator = math.sqrt(sum((min_rank_values[i] - mean_min_rank)**2 for i in range(n))) * math.sqrt(sum((comm_complexity_values[i] - mean_comm_complexity)**2 for i in range(n)))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm_complexity,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": "" if correlation_coefficient > 0.5 else "low_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "low_correlation" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] == "low_correlation")
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")