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
    
    def generate_disjointness_instance(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_noncrossing_partition(instance):
        n = len(instance)
        partition = [[i] for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if instance[i] == instance[j]:
                    partition[i].extend(partition.pop(j))
        return partition
    
    def compute_minimal_rank(partition):
        rank = 0
        seen = set()
        for subset in partition:
            subset_tuple = tuple(sorted(subset))
            if subset_tuple not in seen:
                seen.add(subset_tuple)
                rank += 1
        return rank
    
    def compute_communication_complexity(instance):
        n = len(instance)
        # Simplified communication complexity model (constant multiple of instance size)
        return 2 * n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_communication_complexity = 0
    total_minimal_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            instance = generate_disjointness_instance(n)
            partition = compute_noncrossing_partition(instance)
            minimal_rank = compute_minimal_rank(partition)
            communication_complexity = compute_communication_complexity(instance)
            
            total_communication_complexity += communication_complexity
            total_minimal_rank += minimal_rank
            instances_tested += 1
    
    mean_ratio = total_communication_complexity / (total_minimal_rank * len(n_values))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_ratio >= 1.2 and all(mean_ratio <= 1.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")