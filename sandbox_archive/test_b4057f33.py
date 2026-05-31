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
    
    def circuit_satisfiability_time(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if all(f[i ^ j] == f[j] for j in range(i)):
                count += 1
        return count
    
    def permutation_group_size(f):
        n = int(math.log2(len(f)))
        assignments = [i for i in range(2**n) if all(f[i ^ j] == f[j] for j in range(i))]
        group = set()
        for a in assignments:
            for b in assignments:
                if all(f[a ^ b] == f[b] for b in assignments):
                    group.add((a, b))
        return len(group)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            t_f = circuit_satisfiability_time(f)
            G_f = permutation_group_size(f)
            results.append({
                "n": n,
                "t_f": t_f,
                "G_f": G_f
            })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    t_f_values = [result["t_f"] for result in results]
    G_f_values = [result["G_f"] for result in results]
    
    mean_t_f = sum(t_f_values) / len(t_f_values)
    mean_G_f = sum(G_f_values) / len(G_f_values)
    
    correlation = 0
    if mean_t_f > 0 and mean_G_f > 0:
        numerator = sum((t_f - mean_t_f) * (G_f - mean_G_f) for t_f, G_f in zip(t_f_values, G_f_values))
        denominator = math.sqrt(sum((t_f - mean_t_f)**2 for t_f in t_f_values)) * math.sqrt(sum((G_f - mean_G_f)**2 for G_f in G_f_values))
        correlation = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation) > 0.1,  # Threshold for significance
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")