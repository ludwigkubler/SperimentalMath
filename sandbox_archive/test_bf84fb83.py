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
    
    def resolution_width(f):
        n = len(f)
        clauses = []
        for i in range(n):
            clause = []
            for j in range(2**(n-1)):
                if f[j] == 1 and f[j | (1 << i)] == 0:
                    clause.append(j + 1)
                    clause.append(-(j | (1 << i)) - 1)
            clauses.append(clause)
        return len(clauses)
    
    def noncrossing_partition(n):
        if n == 1:
            return [[1]]
        partitions = []
        for i in range(1, n):
            left_partitions = noncrossing_partition(i)
            right_partitions = noncrossing_partition(n - i)
            for left in left_partitions:
                for right in right_partitions:
                    partitions.append([left + [n], right])
        return partitions
    
    def min_rank(partition):
        rank = 0
        for block in partition:
            rank += len(block)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    min_ranks = []
    widths = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            width = resolution_width(f)
            partition = noncrossing_partition(n)
            rank = min_rank(partition)
            min_ranks.append(rank)
            widths.append(width)
            total_instances += 1
    
    if not min_ranks or not widths:
        return {
            "metric_name": "min_rank_to_resolution_ratio",
            "metric_value": None,
            "instances_tested": total_instances,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    ratio_mean = mean_rank / mean_width
    
    if 1.4 <= ratio_mean <= 1.6:
        return {
            "metric_name": "min_rank_to_resolution_ratio",
            "metric_value": ratio_mean,
            "instances_tested": total_instances,
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "min_rank_to_resolution_ratio",
            "metric_value": ratio_mean,
            "instances_tested": total_instances,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Ratio {ratio_mean} not in [1.4, 1.6]"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=NA support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"Ratio out of [1.4, 1.6]\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)