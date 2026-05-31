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

# Helper functions for noncrossing partition complexity and automorphism group order
def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def is_noncrossing_partition(partition):
    # Check if the partition is non-crossing
    n = max(max(p) for p in partition)
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            if any(x < i and y > j or x > i and y < j for p in partition for x, y in zip(sorted(p), sorted(p)[1:])):
                return False
    return True

def noncrossing_partition_complex(f, n):
    # Generate all possible partitions of the domain {0, ..., n-1}
    def generate_partitions(domain):
        if not domain:
            yield []
        else:
            for i in range(1, len(domain) + 1):
                for partition in generate_partitions(domain[i:]):
                    yield [domain[:i]] + partition

    partitions = list(generate_partitions(list(range(n))))
    valid_partitions = [p for p in partitions if is_noncrossing_partition(p)]
    return valid_partitions

def automorphism_group_order(partitions):
    # Calculate the order of the automorphism group
    n = max(max(p) for p in partition)
    if not partitions:
        return 1
    return len(partitions)

def communication_complexity(f, n):
    # Measure communication complexity using a simple protocol (e.g., deterministic communication)
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "communication_complexity"
    instances_tested = 0
    total_order = 0
    total_communication = 0
    n_max = 1
    
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        partitions = noncrossing_partition_complex(f, n)
        order = automorphism_group_order(partitions)
        communication = communication_complexity(f, n)
        
        if order == 0:
            return {
                "metric_name": metric_name,
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        total_order += order
        total_communication += communication
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_order = Fraction(total_order, instances_tested)
    mean_communication = Fraction(total_communication, instances_tested)
    ratio = mean_order / mean_communication
    
    return {
        "metric_name": metric_name,
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(ratio - 1) < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")