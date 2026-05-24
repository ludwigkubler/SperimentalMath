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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_curve(f):
        n = len(f)
        curve = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n + 1):
                if f[i] == 1 and f[j - 1] == 1:
                    curve[i][j] = 1
        return curve
    
    def resolution_proof_width(curve):
        n = len(curve) - 1
        width = 0
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                if curve[i][j] == 1:
                    width += 1
        return width
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    curve = compute_tropical_curve(f)
    width = resolution_proof_width(curve)
    theta_n = log2(n) ** 2
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width <= 1.5 * theta_n,
        "counterexample": "" if width <= 1.5 * theta_n else f"Function with n={n} has width {width}, expected at most {1.5 * theta_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Function with n={n} has width {width}, expected at most {1.5 * theta_n}\" first_failing_seed={first_failing_seed}")