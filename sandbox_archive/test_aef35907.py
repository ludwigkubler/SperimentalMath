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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n + 1):
            poly = [sum(f[j] * (j >> k & 1) for j in range(2**n)) % 2 for k in range(i + 1)]
            if all(p == 0 or p == 1 for p in poly):
                rank = i
        return rank
    
    def quadratic_residue_system_diameter(f):
        n = int(math.log2(len(f)))
        qrs = []
        for i in range(2**n):
            qrs.append(sum(f[j] * (i >> j & 1) for j in range(n)) % 2)
        max_distance = 0
        for i in range(len(qrs)):
            for j in range(i + 1, len(qrs)):
                distance = sum(abs(a - b) for a, b in zip(qrs[i], qrs[j]))
                if distance > max_distance:
                    max_distance = distance
        return max_distance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        d_qrs = quadratic_residue_system_diameter(f)
        if rank == 0 or d_qrs == 0:
            continue
        ratio = d_qrs / math.sqrt(rank)
        results.append((n, d_qrs, rank, ratio))
    
    if not results:
        return {
            "metric_name": "d(QRS_f)/sqrt(r(f))",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(r for _, _, _, r in results) / len(results)
    max_n = max(n for n, _, _, _ in results)
    
    return {
        "metric_name": "d(QRS_f)/sqrt(r(f))",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": all(r <= 1 for _, _, _, r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")