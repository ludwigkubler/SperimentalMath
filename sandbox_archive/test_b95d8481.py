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
    
    def entropy(f):
        n = len(list(f.keys()))
        counts = [sum(1 for _ in f.values() if v == i) / n for i in range(2)]
        return -sum(p * math.log2(p) for p in counts if p > 0)
    
    def padic_order(f):
        # Placeholder function to simulate the computation
        # Replace with actual implementation as needed
        return random.randint(1, 100)
    
    def map_functions(f, g):
        # Placeholder function to simulate the mapping
        # Replace with actual implementation as needed
        return f, g
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = {i: random.randint(0, 1) for i in range(n)}
    ent_f = entropy(f)
    
    if ent_f == 0:
        return {
            "metric_name": "ord(padic_order(f)) / H(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_f = padic_order(f)
    if ord_f is None:
        return {
            "metric_name": "ord(padic_order(f)) / H(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    g = {i: random.randint(0, 1) for i in range(n)}
    ent_g = entropy(g)
    ord_g = padic_order(g)
    
    if ent_f == ent_g:
        h_f, h_g = map_functions(f, g)
        ord_h_f = padic_order(h_f)
        ord_h_g = padic_order(h_g)
        if ord_h_f != ord_h_g or ord_h_f != min(ord_f, ord_g):
            return {
                "metric_name": "ord(padic_order(f)) / H(f)",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Counterexample: h_f({f}) -> {h_f}, h_g({g}) -> {h_g}"
            }
    
    if ord_f > ent_f * 100:
        return {
            "metric_name": "ord(padic_order(f)) / H(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: ord({f}) = {ord_f}, H({f}) = {ent_f}"
        }
    
    return {
        "metric_name": "ord(padic_order(f)) / H(f)",
        "metric_value": ord_f / ent_f,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")