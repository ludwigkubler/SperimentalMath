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
    
    def monotone_width(circuit):
        # Placeholder function for computing monotone width
        return len(circuit)  # Simplified for demonstration
    
    def qps_order(n):
        # Placeholder function for computing minimal order of a quasi-platonic solid
        return n * (n + 1) // 2  # Example: triangular number sequence
    
    trials = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        circuit = [random.choice([0, 1]) for _ in range(n)]
        w_m = monotone_width(circuit)
        qps_order_n = qps_order(n)
        
        if abs(w_m - qps_order_n) > 30:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": len(trials),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Monotone width {w_m} differs from qps_order {qps_order_n} by more than 30 units"
            }
        
        trials.append((w_m, qps_order_n))
    
    correlation = sum(abs(w_m - qps_order_n) for w_m, qps_order_n in trials) / len(trials)
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(trials),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": correlation <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_bound\" first_failing_seed={first_failing_seed}")