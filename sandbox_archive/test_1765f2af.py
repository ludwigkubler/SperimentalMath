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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(f):
        n = int(math.log2(len(f)))
        width = 0
        for i in range(n):
            if any(f[j] == 1 and f[j ^ (1 << k)] == 0 for j in range(2**n) for k in range(i)):
                width += 1
        return width
    
    def quotient_algebra_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            if any(f[j] == 1 and f[j ^ (1 << k)] == 0 for j in range(2**n) for k in range(i)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            width = monotone_width(f)
            rank = quotient_algebra_rank(f)
            if rank > 5 * width:
                return {
                    "metric_name": "quotient_algebra_rank",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"rank={rank} > 5 * width={width}"
                }
            total_rank += rank
            total_width += width
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * width for rank, width in zip([mean_rank] * instances_tested, [mean_width] * instances_tested)) - instances_tested * mean_rank * mean_width) / ((instances_tested - 1) * math.sqrt(instances_tested * sum((rank - mean_rank)**2 for rank in [mean_rank] * instances_tested) - (instances_tested * mean_rank**2)))
    
    return {
        "metric_name": "quotient_algebra_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_rank <= 5 * mean_width,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > 5 * width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")