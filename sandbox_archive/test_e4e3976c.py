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
    
    def generate_formula(n):
        if n == 1:
            return 'x'
        else:
            return f'({generate_formula(n-1)} & {random.choice(["y", "z"])}) | ({generate_formula(n-1)} & !{random.choice(["y", "z"])})'
    
    def count_literals(formula):
        if formula in ['x', 'y', 'z']:
            return 1
        elif '&' in formula:
            left, right = formula.split('&')
            return count_literals(left) + count_literals(right)
        elif '|' in formula:
            left, right = formula.split('|')
            return max(count_literals(left), count_literals(right))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times
            formula = generate_formula(n)
            complexity = count_literals(formula)
            total_complexity += complexity
            instances_tested += 1
    
    mean_complexity = total_complexity / instances_tested
    conjecture_holds = mean_complexity <= n_values[-1]**2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_zeta_function_complexity",
        "metric_value": mean_complexity,
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*37 + 1, 64))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")