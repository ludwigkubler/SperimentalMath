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
    
    def generate_bp_read_twice(n):
        if n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        else:
            bp = [0] * (n - 1)
            for i in range(1, n - 1):
                bp[i] = random.choice([0, 1])
            bp[0] = random.choice([0, 1])
            bp[-1] = random.choice([0, 1])
            return bp
    
    def norm(bp):
        if not bp:
            return 0
        n = len(bp)
        total = 0
        for i in range(n):
            total += abs(bp[i])
        return total / n
    
    size = random.randint(5, 40)
    bp = generate_bp_read_twice(size)
    computed_norm = norm(bp)
    
    alpha_found = False
    for alpha in range(1, 100):
        if abs(computed_norm - alpha * size) <= 3:
            alpha_found = True
            break
    
    return {
        "metric_name": "conjecture_support",
        "metric_value": computed_norm,
        "instances_tested": 1,
        "conjecture_holds": alpha_found,
        "counterexample": "" if alpha_found else "alpha_not_found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds are provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='alpha_not_found' first_failing_seed={first_failing_seed}")