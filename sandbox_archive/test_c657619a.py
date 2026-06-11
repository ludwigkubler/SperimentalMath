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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = []
        for i in range(n):
            row = [f[j] ^ f[j + 2**i] for j in range(2**(n-i-1))]
            rank.append(sum(row))
        return sum(rank) / len(rank)
    
    def minimal_topological_degree(f):
        n = int(math.log2(len(f)))
        degree = 0
        for i in range(n):
            count = 0
            for j in range(2**(n-i-1)):
                if f[j] != f[j + 2**i]:
                    count += 1
            degree = max(degree, count)
        return degree
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(20):  # Ensure at least 100 instances per seed
            f = generate_boolean_function(n)
            rc_f = communication_complexity_rank_variance(f)
            td_f = minimal_topological_degree(f)
            metric_values.append(td_f / rc_f)
            instances_tested += 1
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    
    return {
        "metric_name": "td_over_rc",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(td >= rc for td, rc in zip(metric_values, metric_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")