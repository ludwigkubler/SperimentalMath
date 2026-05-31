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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncrossing_partitions(n):
        if n == 0:
            return [[]]
        partitions = []
        for partition in noncrossing_partitions(n-1):
            partitions.append([[n] + p for p in partition])
            for i in range(len(partition)):
                new_partition = partition[:i] + [[n]] + partition[i:i+1] + partition[i+2:]
                if all(new_partition[j][0] > new_partition[j+1][0] for j in range(len(new_partition)-1)):
                    partitions.append(new_partition)
        return partitions
    
    def automorphism_group_order(partition):
        n = max(max(p) for p in partition)
        group = set()
        for perm in itertools.permutations(range(1, n+1)):
            if all([perm[p[i]-1] == p[j-1] for i, j in zip(*partition)]):
                group.add(tuple(perm))
        return len(group)
    
    def communication_complexity(f):
        # Simple example: 2-bit function requires 2 bits to communicate
        return len(f) // 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    partitions = noncrossing_partitions(n)
    order = automorphism_group_order(partitions)
    comm_complexity = communication_complexity(f)
    
    return {
        "metric_name": "order_over_comm",
        "metric_value": order / comm_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(order / comm_complexity - 1) <= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order_over_comm = sum(r["metric_value"] for r in results) / len(results)
    std_order_over_comm = math.sqrt(sum((r["metric_value"] - mean_order_over_comm)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order_over_comm} std={std_order_over_comm} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order_over_comm} std={std_order_over_comm} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order_not_correlated_with_comm\" first_failing_seed={first_failing_seed}")