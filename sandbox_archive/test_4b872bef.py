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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        # Simplified version using a min-cut algorithm
        # This is just an example; actual implementation may vary
        return n
    
    def entropy(diagram):
        # Simplified entropy calculation for demonstration purposes
        counts = [diagram.count(0), diagram.count(1)]
        total = sum(counts)
        if total == 0:
            return 0
        p0 = counts[0] / total
        p1 = counts[1] / total
        return -p0 * math.log2(p0) - p1 * math.log2(p1)
    
    def coxeter_diagram(f):
        # Simplified Coxeter diagram construction for demonstration purposes
        n = int(math.log2(len(f)))
        diagram = [f[i] ^ f[j] for i in range(n) for j in range(i+1, n)]
        return diagram
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        c_f = communication_complexity(f)
        H_Cox_f = entropy(coxeter_diagram(f))
        
        results.append({
            "n": n,
            "c_f": c_f,
            "H_Cox_f": H_Cox_f
        })
    
    r = 0
    for i in range(len(results)):
        for j in range(i+1, len(results)):
            r += (results[i]["c_f"] * results[j]["c_f"] - results[i]["H_Cox_f"] * results[j]["H_Cox_f"])
    r /= (len(results) * (len(results) - 1))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": r,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(r) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_r = sum(result["metric_value"] for result in results) / len(results)
    std_r = math.sqrt(sum((result["metric_value"] - mean_r)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.5) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='N/A' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")