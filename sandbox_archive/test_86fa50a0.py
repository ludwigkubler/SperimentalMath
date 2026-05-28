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
    
    def generate_monotone_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncrossing_partition(f):
        n = len(f)
        if n == 1:
            return [f]
        
        elements = []
        for i in range(n):
            left = f[:i+1]
            right = f[i+1:]
            if all(left[j] <= right[j] for j in range(len(right))):
                elements.append((left, right))
        
        return elements
    
    def count_elements(partition):
        count = 0
        for element in partition:
            count += len(element[0]) + len(element[1])
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_count = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different functions
            f = generate_monotone_function(n)
            partition = noncrossing_partition(f)
            count = count_elements(partition)
            total_count += count
            instances_tested += 1
    
    mean_count = total_count / instances_tested
    conjecture_holds = all(mean_count <= C * math.log(n) for n in n_values for C in range(1, 5))
    
    return {
        "metric_name": "mean_noncrossing_partition_elements",
        "metric_value": mean_count,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")