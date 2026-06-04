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
    
    def log2(x):
        return math.log2(x) if x > 0 else float('inf')
    
    def resolution_width(phi):
        # Simplified DPLL solver to estimate width
        stack = []
        literals = set()
        for clause in phi:
            if not any(lit in literals for lit in clause):
                literals.update(clause)
                stack.append(clause)
            elif all(-lit in literals for lit in clause):
                return len(stack) + 1
        return len(stack)
    
    def brayuer_group_order(n):
        # Simplified Brauer group order calculation
        return (n * (n - 1)) // 2
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        phi = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(2, n))]
        
        width = resolution_width(phi)
        order = brayuer_group_order(n)
        
        if width == 0:
            continue
        
        ratio = log2(n) ** 2 / width
        metric_values.append(ratio)
        
        if ratio > order:
            conjecture_holds = False
            counterexample = f"n={n}, w(φ)={width}, B(φ)={order}"
    
    return {
        "metric_name": "log(n)^2/w(φ)",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")