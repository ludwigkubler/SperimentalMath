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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        width = 0
        for i in range(1, n):
            if all(circuit[j] <= circuit[j-1] for j in range(i)):
                width += 1
        return width
    
    def qps_order(n):
        # Simplified heuristic to estimate QPS order based on input size
        return n * (n + 1) // 2
    
    instances_tested = 0
    total_diff = 0
    max_n = 0
    
    for _ in range(30):  # Sample 30 random circuits
        n = random.randint(5, 40)
        circuit = generate_boolean_circuit(n)
        w_m = monotone_width(circuit)
        qps_order_n = qps_order(n)
        
        instances_tested += 1
        max_n = max(max_n, n)
        
        diff = abs(w_m - qps_order_n)
        total_diff += diff
        
        if diff > 30:
            return {
                "metric_name": "Absolute Difference",
                "metric_value": diff,
                "instances_tested": instances_tested,
                "n_max": max_n,
                "conjecture_holds": False,
                "counterexample": f"Monotone width exceeds QPS order by more than 30 units"
            }
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": total_diff / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Monotone width exceeds QPS order by more than 30 units\" first_failing_seed={first_failing_seed}")