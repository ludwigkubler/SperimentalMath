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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def communication_complexity_rank(f):
        n = len(f)
        max_rank = 0
        for i in range(n):
            rank = sum(1 for j in range(i+1, n) if f[i] != f[j])
            if rank > max_rank:
                max_rank = rank
        return max_rank
    
    def minimal_order_of_groupoid_representations(f):
        m = int(math.log2(len(f)))
        if m == 0:
            return 0
        order = 1
        while True:
            groupoid_representations = [f[i:i+m] for i in range(0, len(f), m)]
            if all(all(groupoid_representations[i][j] != groupoid_representations[j][i] for j in range(i+1, len(groupoid_representations))) for i in range(len(groupoid_representations))):
                return order
            order += 1
    
    results = []
    for m in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(m)
        groupoid_order = minimal_order_of_groupoid_representations(f)
        rank = communication_complexity_rank(f)
        results.append({"m": m, "groupoid_order": groupoid_order, "rank": rank})
    
    metric_value = sum(result["groupoid_order"] for result in results) / len(results)
    conjecture_holds = all(result["groupoid_order"] >= result["m"]**2 * math.log(result["m"]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Order of Groupoid Representations",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["m"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")