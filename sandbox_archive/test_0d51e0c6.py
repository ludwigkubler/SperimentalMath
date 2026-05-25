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
    
    def generate_bp(n):
        bp = [0] * n
        for i in range(1, n):
            if random.choice([True, False]):
                bp[i] = 1 - bp[i-1]
            else:
                bp[i] = bp[i-1]
        return bp
    
    def noncrossing_partition(bp):
        n = len(bp)
        partition = []
        for i in range(n):
            if bp[i] == 0:
                partition.append([i])
            else:
                for j in range(len(partition) - 1, -1, -1):
                    if partition[j][-1] < i and (j == 0 or partition[j-1][-1] >= i):
                        partition[j].append(i)
                        break
        return partition
    
    def rank_of_partition(partition):
        n = len(partition)
        rank = [0] * n
        for i in range(n):
            rank[i] = max([len(p) for p in partition if i in p])
        return sum(rank)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        bp = generate_bp(n)
        partition = noncrossing_partition(bp)
        rank = rank_of_partition(partition)
        
        if len(partition) == 0:
            return {
                "metric_name": "rank_over_log_size",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "empty_partition"
            }
        
        results.append((n, rank))
    
    mean_rank = sum(rank for n, rank in results) / len(results)
    std_dev = math.sqrt(sum((rank - mean_rank)**2 for n, rank in results) / len(results))
    ratio_mean = mean_rank / math.log(mean_rank[0])
    ratio_std = std_dev / math.log(mean_rank[0])
    
    return {
        "metric_name": "rank_over_log_size",
        "metric_value": ratio_mean,
        "instances_tested": 30,
        "conjecture_holds": ratio_mean <= 1 and ratio_std < 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 50, 2))
    
    total_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        total_results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in total_results) / len(total_results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in total_results) / len(total_results))
    support_fraction = sum(1 for r in total_results if r["conjecture_holds"]) / len(total_results)
    
    if all(r["conjecture_holds"] for r in total_results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in total_results):
        first_failing_seed = next(seed for seed, r in zip(seeds, total_results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_exceeds_log_size\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")