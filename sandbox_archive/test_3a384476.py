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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def calculate_entropy(f):
        counts = [f.count(i) / len(f) for i in [0, 1]]
        entropy = -sum(p * math.log2(p) if p != 0 else 0 for p in counts)
        return entropy
    
    def calculate_quotient_algebra_order(f):
        n = int(math.log2(len(f)))
        order = 1
        while True:
            found = False
            for i in range(1, n+1):
                if all(f[j] == f[j+i] for j in range(0, len(f), 2*i)):
                    order *= i
                    found = True
                    break
            if not found:
                break
        return order
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        entropy = calculate_entropy(f)
        order = calculate_quotient_algebra_order(f)
        results.append({"n": n, "entropy": entropy, "order": order})
    
    if len(results) < 15:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    entropy_values = [r["entropy"] for r in results]
    order_values = [r["order"] for r in results]
    mean_entropy = sum(entropy_values) / len(entropy_values)
    mean_order = sum(order_values) / len(order_values)
    
    correlation_coefficient = 0
    if mean_entropy != 0 and mean_order != 0:
        numerator = sum((e - mean_entropy) * (o - mean_order) for e, o in zip(entropy_values, order_values))
        denominator = math.sqrt(sum((e - mean_entropy)**2 for e in entropy_values)) * math.sqrt(sum((o - mean_order)**2 for o in order_values))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")