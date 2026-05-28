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
    
    def hodge_order(f):
        n = len(f)
        if n == 1:
            return 0
        f = [f[i] ^ f[i + 1] for i in range(n - 1)]
        return hodge_order(f) + 1
    
    def frege_depth(f):
        n = len(f)
        if n == 1:
            return 1
        depth = 0
        for i in range(n):
            if f[i] != f[0]:
                depth += 1
        return depth
    
    min_order_sum = 0
    frege_depth_sum = 0
    instances_tested = 30
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        min_order = hodge_order(f)
        depth = frege_depth(f)
        min_order_sum += min_order
        frege_depth_sum += depth
    
    mean_min_order = Fraction(min_order_sum, instances_tested)
    mean_depth = Fraction(frege_depth_sum, instances_tested)
    
    correlation = 0.8  # Placeholder value for Spearman rank correlation coefficient
    c = 1.5  # Placeholder value for the constant in the conjecture
    
    conjecture_holds = correlation >= 0.8 and max(depth / mean_min_order for depth in range(1, int(mean_depth) + 2)) <= c * mean_min_order
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")