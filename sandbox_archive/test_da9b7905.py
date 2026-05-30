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
    
    def generate_instance(n):
        return {i: random.choice([0, 1]) for i in range(2**n)}
    
    def compute_simplices(instance):
        n = len(instance)
        simplices = []
        for k in range(n + 1):
            for comb in itertools.combinations(range(n), k):
                simplices.append(list(comb))
        return simplices
    
    def compute_euler_characteristic(instance):
        simplices = compute_simplices(instance)
        dim = len(simplices) - 1
        euler_char = 0
        for i in range(dim + 1):
            if i % 2 == 0:
                euler_char += len([s for s in simplices if len(s) == i])
            else:
                euler_char -= len([s for s in simplices if len(s) == i])
        return euler_char
    
    def compute_protocol_complexity(instance):
        n = len(instance)
        protocol_complexity = 0
        for k in range(n + 1):
            for comb in itertools.combinations(range(n), k):
                protocol_complexity += 1
        return protocol_complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_euler_char = 0.0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            instance = generate_instance(n)
            euler_char = compute_euler_characteristic(instance)
            protocol_complexity = compute_protocol_complexity(instance)
            instances_tested += 1
            total_euler_char += euler_char
            max_n = max(max_n, n)
    
    mean_euler_char = total_euler_char / instances_tested
    
    conjecture_holds = abs(mean_euler_char - protocol_complexity) <= 2 * math.sqrt(protocol_complexity)
    counterexample = "" if conjecture_holds else f"mean_euler_char={mean_euler_char}, protocol_complexity={protocol_complexity}"
    
    return {
        "metric_name": "Euler characteristic",
        "metric_value": mean_euler_char,
        "instances_tested": instances_tested,
        "n_max": max_n,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_euler_char does not match protocol_complexity\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")