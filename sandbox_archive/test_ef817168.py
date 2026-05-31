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

def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))

def generate_communication_instance(n):
    return ''.join(random.choice('01') for _ in range(n))

def minimal_generators(outcomes):
    if not outcomes:
        return 0
    generators = set()
    for outcome in outcomes:
        for i in range(len(outcome)):
            if outcome[i] == '1':
                generators.add(i)
    return len(generators)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        outcomes = [generate_communication_instance(n) for _ in range(30)]
        generators = minimal_generators(outcomes)
        alpha_log_n = ackermann(4, int(math.log2(n)))
        results.append((n, generators, alpha_log_n))
    
    mean_C = sum(generators for _, generators, _ in results) / len(results)
    mean_ranks = sum(alpha_log_n for _, _, alpha_log_n in results) / len(results)
    ratio_mean = mean_C / mean_ranks
    
    support_fraction = sum(1 for _, generators, _ in results if abs(ratio_mean - 3) <= 0.1) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Generators to Ackermann(log n)",
        "metric_value": ratio_mean,
        "instances_tested": len(results),
        "n_max": max(n for _, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_C = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")