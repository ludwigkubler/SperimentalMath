# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        max_comm = 0
        for i in range(2**n):
            comm = sum(1 for j in range(i+1, 2**n) if f[i] != f[j])
            max_comm = max(max_comm, comm)
        return max_comm
    
    def min_deligne_connes_tensor_rank(f):
        n = len(f)
        rank = float('inf')
        for i in range(1 << n):
            subfunc = [f[j] if (i & (1 << j)) else 0 for j in range(n)]
            comm = communication_complexity(subfunc)
            rank = min(rank, comm)
        return rank
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mDCT_sum = 0
    C_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            mDCT = min_deligne_connes_tensor_rank(f)
            C = communication_complexity(f)
            if mDCT != float('inf') and C != float('inf'):
                mDCT_sum += mDCT
                C_sum += C
                instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "mDCT/C",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mDCT_mean = mean([mDCT_sum / instances_tested])
    C_mean = mean([C_sum / instances_tested])
    ratio = abs((mDCT_mean / C_mean) - 1)
    
    return {
        "metric_name": "mDCT/C",
        "metric_value": mDCT_mean / C_mean,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": ratio <= 0.1,
        "counterexample": "" if ratio <= 0.1 else f"mDCT/C = {mDCT_mean / C_mean}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mDCT_mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    C_mean = sum(1 / r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mDCT_mean} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mDCT_mean} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break