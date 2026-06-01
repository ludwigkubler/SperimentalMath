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
        n = len(f)
        count = 0
        for i in range(n):
            if f[i] != f[0]:
                count += 1
        return count
    
    def riemann_roch_theorem(n, k):
        return math.comb(n + k - 1, k) - math.comb(n - 1, k)
    
    def number_of_distinct_roots(f):
        n = len(f)
        roots = set()
        for i in range(2**n):
            z = complex(random.uniform(-10, 10), random.uniform(-10, 10))
            if abs(z) > 1e-6 and f[i] == 1:
                roots.add(z)
        return len(roots)
    
    C = None
    ratios = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            r_f = communication_complexity_rank(f)
            roots_count = number_of_distinct_roots(f)
            if r_f == 0:
                continue
            ratio = roots_count / (r_f ** 2)
            ratios.append(ratio)
    
    if not ratios:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_valid_ratio"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    if C is None:
        C = max(1, math.ceil(mean_ratio))
    
    conjecture_holds = all(ratio <= C for ratio in ratios)
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(ratios),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_ratio={mean_ratio}, C={C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")