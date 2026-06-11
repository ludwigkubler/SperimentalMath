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
        # Generate a random n-ary communication protocol
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def crossed_product_size(protocol):
        # Constructive mapping to define the crossed product structure
        size = 2 ** len(protocol)
        return size
    
    def rank_variance(protocol):
        # Calculate the communication complexity rank variance R(φ)
        n = len(protocol)
        rank = sum(sum(row) for row in protocol)
        variance = (rank - (n * (n + 1)) / 4) ** 2
        return variance
    
    n_max = 0
    instances_tested = 0
    total_log_min_order = 0
    total_variance = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        protocol = generate_protocol(n)
        min_order = crossed_product_size(protocol)
        variance = rank_variance(protocol)
        
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        total_log_min_order += math.log(min_order)
        total_variance += variance
    
    mean_log_min_order = total_log_min_order / instances_tested
    mean_variance = total_variance / instances_tested
    correlation_coefficient = (instances_tested * total_log_min_order * total_variance -
                                sum(log_min_order * variance for log_min_order, variance in zip(
                                    [math.log(min_order) for min_order in crossed_product_size(generate_protocol(n)) for _ in range(30)],
                                    [rank_variance(generate_protocol(n)) for _ in range(30)]
                                ))) / math.sqrt((instances_tested * sum(math.log(min_order) ** 2 for min_order in crossed_product_size(generate_protocol(n)) for _ in range(30)) - (total_log_min_order ** 2)) *
                                               (instances_tested * sum(rank_variance(generate_protocol(n)) ** 2 for _ in range(30)) - (total_variance ** 2)))
    
    conjecture_holds = correlation_coefficient > 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")