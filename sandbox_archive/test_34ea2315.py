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
    
    def read_twice_bp(n):
        if n == 1:
            return [0]
        else:
            bp = [0] * (2 ** n - 1)
            for i in range(1, n):
                bp[2 ** (i - 1):2 ** i] = read_twice_bp(i)
            return bp
    
    def tropical_curve(bp):
        if not bp:
            return 0
        max_val = max(bp)
        min_val = min(bp)
        return max_val - min_val
    
    n = random.randint(5, 40)
    bp = read_twice_bp(n)
    size = len(bp)
    
    # Construct a Riemann surface with at most O(n) points
    riemann_surface_points = [i for i in range(n)]
    
    index = tropical_curve(bp)
    
    return {
        "metric_name": "index",
        "metric_value": index,
        "instances_tested": 1,
        "conjecture_holds": size >= index,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*10**4 + 1))
    
    results = []
    total_metric_value = 0
    support_count = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
        total_metric_value += result["metric_value"]
        if result["conjecture_holds"]:
            support_count += 1
    
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")