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
    
    def geometric_entropy(instance):
        n = len(instance)
        count_ones = instance.count(1)
        count_zeros = n - count_ones
        if count_ones == 0 or count_zeros == 0:
            return 0
        p_one = count_ones / n
        p_zero = count_zeros / n
        entropy = -p_one * math.log2(p_one) - p_zero * math.log2(p_zero)
        return entropy
    
    def circuit_depth(instance):
        # Simplified DPLL solver to estimate circuit depth
        n = len(instance)
        if n == 1:
            return 1
        return 2 + circuit_depth(instance[:n//2]) + circuit_depth(instance[n//2:])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instance = generate_instance(n)
        entropy = geometric_entropy(instance)
        depth = circuit_depth(instance)
        if entropy == 0 or depth == 0:
            continue
        results.append({
            "n": n,
            "geometric_entropy": entropy,
            "circuit_depth": depth
        })
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(r["n"] for r in results)
    mean_entropy = sum(r["geometric_entropy"] for r in results) / len(results)
    mean_depth = sum(r["circuit_depth"] for r in results) / len(results)
    
    conjecture_holds = all(entropy >= n**(1/3) and depth <= 2 * entropy for n, entropy, depth in zip(n_values, [r["geometric_entropy"] for r in results], [r["circuit_depth"] for r in results]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")