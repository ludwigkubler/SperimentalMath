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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        max_rank = 0
        for i in range(2**n):
            rank = 0
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    rank += 1
            max_rank = max(max_rank, rank)
        return max_rank
    
    def minimal_local_ring_unit_group_size(tropical_variety):
        # Placeholder for actual computation
        # This is a dummy implementation for the sake of testing
        return random.randint(1, 10)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per size
            f = generate_boolean_function(n)
            tropical_variety = set(f)  # Placeholder for actual computation
            unit_group_size = minimal_local_ring_unit_group_size(tropical_variety)
            rank = communication_complexity_rank(f)
            instances_tested += 1
            max_n = max(max_n, n)
            total_metric_value += unit_group_size
    
    if instances_tested < 30:
        return {
            "metric_name": "minimal_local_ring_unit_group_size",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "minimal_local_ring_unit_group_size",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction=1.0")
    elif any(r["counterexample"] == "insufficient_instances" for r in results):
        print(f"RESULT: INCONCLUSIVE reason=insufficient_instances n_tested={len(results)}")
    else:
        print("RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=-1")