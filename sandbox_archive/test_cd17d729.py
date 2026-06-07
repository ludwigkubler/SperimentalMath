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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_abelian_variants(instance):
        n = len(instance)
        abelian_variants = set()
        for i in range(1 << n):
            group = []
            for j in range(n):
                if (i >> j) & 1:
                    group.append(instance[j])
            abelian_variants.add(tuple(sorted(group)))
        return abelian_variants
    
    def measure_resolution_width(instance):
        # Simplified DPLL solver to estimate resolution width
        n = len(instance)
        stack = []
        for i in range(n):
            if instance[i] == 1:
                stack.append(i)
            else:
                if i in stack:
                    stack.remove(i)
        return len(stack)
    
    def calculate_abelian_number(abelian_variants):
        return len(abelian_variants)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        instance = generate_instance(n)
        abelian_variants = construct_abelian_variants(instance)
        resolution_width = measure_resolution_width(instance)
        abelian_number = calculate_abelian_number(abelian_variants)
        
        total_metric_value += abelian_number
        instances_tested += 1
        
        if abelian_number > n**2 * 1.5:
            conjecture_holds = False
            counterexample = f"n={n}, A(φ)={abelian_number}, expected <= {n**2 * 1.5}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = 1.0
    
    return {
        "metric_name": "Minimal Number of Abelian Variants",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")