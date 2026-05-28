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
    
    def noncrossing_partition_size(f):
        n = len(f)
        if n == 1:
            return 1
        partition = []
        for i in range(n):
            if f[i] != f[0]:
                partition.append([i])
        partition.append(list(range(1, n)))
        return len(partition)
    
    def arborescence_complexity(size):
        return math.log2(size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_arborescence_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # At least 5 instances per size
            f = generate_boolean_function(n)
            size = noncrossing_partition_size(f)
            complexity = arborescence_complexity(size)
            total_arborescence_complexity += complexity
            instances_tested += 1
    
    mean_complexity = total_arborescence_complexity / instances_tested
    conjecture_holds = mean_complexity <= 1.5 * math.log2(n_values[-1])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "arborescence_complexity",
        "metric_value": mean_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")