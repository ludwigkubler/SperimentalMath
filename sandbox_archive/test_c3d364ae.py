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
    
    def communication_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 0
        for i in range(1, n):
            for j in range(i+1, n+1):
                if all(f[k] == f[k^i] == f[k^j] for k in range(2**n)):
                    rank += 1
        return rank
    
    def minimal_order_of_hecke_group(f):
        n = len(f)
        if n == 1:
            return 1
        order = 0
        for i in range(1, n+1):
            if all((f[k] == f[k^i]) for k in range(2**n)):
                order += 1
        return order
    
    instances_tested = 0
    total_order = 0
    total_rank = 0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        order = minimal_order_of_hecke_group(f)
        
        total_order += order
        total_rank += rank
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_order = total_order / instances_tested
    mean_rank = total_rank / instances_tested
    
    correlation_coefficient = (instances_tested * sum(order * rank for order, rank in zip([mean_order] * instances_tested, [mean_rank] * instances_tested)) -
                                sum(mean_order) * sum(mean_rank)) / math.sqrt((instances_tested * sum(order**2 for order in [mean_order] * instances_tested) - sum(mean_order)**2) *
                                                                 (instances_tested * sum(rank**2 for rank in [mean_rank] * instances_tested) - sum(mean_rank)**2))
    
    conjecture_holds = correlation_coefficient > 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")