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
    
    def noncrossing_partition(bp):
        n = len(bp)
        partition = list(range(n))
        for i in range(1, n):
            j = random.randint(i, n-1)
            if j == i:
                continue
            partition.append(partition.pop(j) + partition.pop(j-1))
        return partition
    
    def rank_of_partition(partition):
        n = len(partition)
        rank = 0
        for i in range(n):
            rank += partition[i]
        return rank
    
    max_n = 40
    instances_tested = 0
    total_rank = 0
    support_count = 0
    
    for _ in range(30):
        n = random.randint(5, max_n)
        bp = [random.randint(0, 1) for _ in range(n)]
        partition = noncrossing_partition(bp)
        rank = rank_of_partition(partition)
        
        if rank > math.log(n):
            return {
                "metric_name": "rank/log(size)",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"BP size {n} with rank {rank}"
            }
        
        total_rank += rank
        instances_tested += 1
        if rank <= math.log(n):
            support_count += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    std_dev = math.sqrt(sum((rank - mean_rank)**2 for rank in range(instances_tested)) / instances_tested)
    
    if support_count >= 0.8 * instances_tested:
        return {
            "metric_name": "rank/log(size)",
            "metric_value": float(mean_rank),
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "rank/log(size)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"Counterexample found with rank {mean_rank} and std_dev {std_dev}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(supported_count, len(results))
    
    if all(r["metric_value"] is not None for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
        
        if support_fraction >= Fraction(4, 5):
            print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE some trials had no metric value")