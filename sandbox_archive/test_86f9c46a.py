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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def hdim(G):
        # Placeholder function for minimal Hodge theoretical dimension
        # This is a dummy implementation and should be replaced with actual computation
        return len(G) / 2
    
    def ccr(G):
        # Placeholder function for communication complexity rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(G)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_graph(n)
        hdim_value = hdim(G)
        ccr_value = ccr(G)
        results.append((hdim_value, ccr_value))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    hdim_values = [r[0] for r in results]
    ccr_values = [r[1] for r in results]
    
    n = len(hdim_values)
    mean_hdim = sum(hdim_values) / n
    mean_ccr = sum(ccr_values) / n
    
    cov = sum((h - mean_hdim) * (c - mean_ccr) for h, c in zip(hdim_values, ccr_values)) / n
    var_hdim = sum((h - mean_hdim) ** 2 for h in hdim_values) / n
    var_ccr = sum((c - mean_ccr) ** 2 for c in ccr_values) / n
    
    correlation_coefficient = cov / (math.sqrt(var_hdim) * math.sqrt(var_ccr))
    
    p_value = 2 * (1 - abs(correlation_coefficient)) if correlation_coefficient >= 0 else 2 * abs(correlation_coefficient)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.8 and p_value < 0.05,
        "counterexample": f"correlation_coefficient={correlation_coefficient}, p_value={p_value}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")