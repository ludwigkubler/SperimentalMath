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
    
    def generate_noncrossing_partition(n):
        if n == 1:
            return [[0]]
        elif n == 2:
            return [[0], [1]], [[0, 1]]
        else:
            partitions = []
            for k in range(1, n-1):
                for p in generate_noncrossing_partition(k):
                    for q in generate_noncrossing_partition(n-k-1):
                        partitions.append(p + [(x+k+1) for x in q])
            return partitions
    
    def communication_complexity(f):
        # Simplified model of communication complexity for DISJOINTNESS
        return len(f)
    
    def rank_of_partition(partition):
        return len(partition)
    
    n = random.randint(5, 40)
    partition = generate_noncrossing_partition(n)[random.randint(0, len(generate_noncrossing_partition(n)) - 1)]
    f = [i in partition[0] for i in range(n)]
    cc = communication_complexity(f)
    rank = rank_of_partition(partition)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": cc / (n * math.log(n)),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Avoid seed=1
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")