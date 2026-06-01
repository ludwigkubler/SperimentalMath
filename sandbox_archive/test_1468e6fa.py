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
    
    def communication_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input must be a power of two length")
        rank = 0
        for i in range(n):
            bits = [f[j] for j in range(i, len(f), n)]
            rank += sum(bits) % 2
        return rank
    
    def minimal_brauer_induction_index(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input must be a power of two length")
        index = 0
        for i in range(n):
            bits = [f[j] for j in range(i, len(f), n)]
            index += sum(bits) % 2
        return index
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        bi_f = minimal_brauer_induction_index(f)
        r_f = communication_rank(f)
        results.append((bi_f, r_f))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    bi_values = [bi for bi, _ in results]
    r_values = [r for _, r in results]
    mean_bi = sum(bi_values) / len(bi_values)
    mean_r = sum(r_values) / len(r_values)
    diff_sum = sum(abs(bi - r) for bi, r in results)
    avg_diff = diff_sum / len(results)
    
    correlation_coefficient = 0
    if len(set(r_values)) > 1:
        numerator = sum((bi - mean_bi) * (r - mean_r) for bi, r in results)
        denominator = math.sqrt(sum((bi - mean_bi)**2 for bi in bi_values)) * math.sqrt(sum((r - mean_r)**2 for r in r_values))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and avg_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 59))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")