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
    
    def compute_matroid(instance):
        matroid = {}
        for i in range(len(instance)):
            if instance[i] == 1:
                matroid[i] = set(range(i + 1))
        return matroid
    
    def noncrossing_partitions(matroid, n):
        partitions = []
        for i in range(1 << n):
            partition = [[]]
            for j in range(n):
                if i & (1 << j):
                    partition[-1].append(j)
                else:
                    partition.append([j])
            partitions.append(partition)
        return partitions
    
    def rank_of_partition(partition, matroid):
        max_rank = 0
        for block in partition:
            block_set = set(block)
            if all(block_set.issubset(matroid[i]) for i in block):
                max_rank = max(max_rank, len(block))
        return max_rank
    
    def communication_complexity(instance):
        n = len(instance)
        count_ones = instance.count(1)
        return 2 * count_ones - 1 if count_ones > 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_disjointness_instance(n)
        matroid = compute_matroid(instance)
        partitions = noncrossing_partitions(matroid, n)
        
        for partition in partitions:
            rank = rank_of_partition(partition, matroid)
            comm_complexity = communication_complexity(instance)
            results.append({
                "n": n,
                "instance": instance,
                "matroid": matroid,
                "partition": partition,
                "rank": rank,
                "comm_complexity": comm_complexity
            })
    
    if not results:
        return {
            "metric_name": "rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_values = [result["rank"] for result in results]
    comm_complexity_values = [result["comm_complexity"] for result in results]
    
    mean_rank = sum(rank_values) / len(rank_values)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in rank_values) / len(rank_values))
    support_fraction = sum(1 for r, cc in zip(rank_values, comm_complexity_values) if r >= n and cc >= n) / len(rank_values)
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if support_fraction == 1.0 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={support_fraction}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")