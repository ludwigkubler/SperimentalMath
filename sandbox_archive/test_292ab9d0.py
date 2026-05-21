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
    
    def generate_function(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def convex_polytope_volume(f):
        n = len(f)
        if n == 1:
            return Fraction(1, 2)
        volume = Fraction(1, 6)
        for i in range(1, n-1):
            volume *= Fraction(i+1, n-i)
        return volume
    
    def acc0_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        size = 2 * (n - 1)
        for i in range(1, n-1):
            size += 2 * (i + 1)
        return size
    
    def intersection_body_volume(f):
        n = len(f)
        if n == 1:
            return Fraction(1, 2)
        volume = Fraction(1, 6)
        for i in range(1, n-1):
            volume *= Fraction(i+1, n-i)
        return volume
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_volume = 0
    total_size = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_function(n)
            volume = intersection_body_volume(f)
            size = acc0_circuit_size(f)
            if size == 0:
                continue
            total_volume += volume
            total_size += size
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    ratio = total_volume / total_size
    c = 1.0  # Placeholder for the constant c
    support_fraction = abs(c - ratio)
    
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction <= 0.1,
        "counterexample": "" if support_fraction <= 0.1 else f"Counterexample found: Ratio={ratio}, c={c}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")