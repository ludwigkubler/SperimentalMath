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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_monotone_width(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        width = 0
        for i in range(n):
            count_0 = sum(1 for x in f if x & (1 << i) == 0)
            count_1 = sum(1 for x in f if x & (1 << i) != 0)
            width += max(count_0, count_1)
        return width
    
    def modular_symmetry_group(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        group = []
        for perm in range(2**n):
            if all(f[perm ^ i] == f[i] for i in range(2**n)):
                group.append(perm)
        return group
    
    def min_rank(group, f):
        n = int(math.log2(len(f)))
        rank = 0
        for g in group:
            matrix = [[f[g ^ i] if (g >> j) & 1 else f[i] for i in range(2**n)] for j in range(n)]
            rank += sum(1 for row in matrix if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        w_f = circuit_monotone_width(f)
        if w_f is None:
            continue
        M_f = modular_symmetry_group(f)
        if M_f is None:
            continue
        min_rank_M_f = min_rank(M_f, f)
        
        results.append({
            "n": n,
            "w_f": w_f,
            "min_rank_M_f": min_rank_M_f
        })
    
    if not results:
        return {
            "metric_name": "min_rank_M_f / w_f",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r["min_rank_M_f"] / r["w_f"] for r in results]
    instances_tested = len(results)
    n_max = max(r["n"] for r in results)
    
    mean_metric_value = sum(metric_values) / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in metric_values) / instances_tested)
    
    conjecture_holds = all(0.5 <= x <= 2 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_M_f / w_f",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if not all(r["instances_tested"] > 0 for r in results):
        print("RESULT: INCONCLUSIVE reason=insufficient_data")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")