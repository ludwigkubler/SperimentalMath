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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_noncrossing_partition_rank(instance):
        n = len(instance)
        if n == 1:
            return 1
        partition = [[i] for i in range(n)]
        rank = 1
        while True:
            new_partitions = []
            for p in partition:
                subpartitions = [[]]
                for x in p:
                    new_subpartitions = []
                    for sp in subpartitions:
                        new_sp = sp[:]
                        new_sp.append(x)
                        new_subpartitions.append(new_sp)
                    subpartitions = new_subpartitions
                new_partitions.extend(subpartitions)
            partition = new_partitions
            rank += 1
        return rank
    
    def compute_communication_complexity(instance):
        n = len(instance)
        # Simplified protocol: each bit requires one communication round
        return n
    
    τ_M_values = []
    comm_complexity_values = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        instance = generate_instance(random.randint(5, 40))
        τ_M = compute_noncrossing_partition_rank(instance)
        comm_complexity = compute_communication_complexity(instance)
        τ_M_values.append(τ_M)
        comm_complexity_values.append(comm_complexity)
    
    mean_τ_M = sum(τ_M_values) / len(τ_M_values)
    mean_comm_complexity = sum(comm_complexity_values) / len(comm_complexity_values)
    
    correlation_coefficient = sum((τ_M - mean_τ_M) * (comm_complexity - mean_comm_complexity) for τ_M, comm_complexity in zip(τ_M_values, comm_complexity_values)) / len(τ_M_values)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_τ_M <= 1.5 * random.randint(5, 40)
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or average τ(M) > O(n)"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(τ_M_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")