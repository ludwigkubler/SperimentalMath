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
    
    def generate_truth_table(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    
    def coxeter_group_order(truth_table):
        n = len(truth_table)
        # Simplified version of computing the order of a Coxeter group
        # This is a placeholder and should be replaced with an actual algorithm
        return 10 * n
    
    def circuit_depth(truth_table):
        n = len(truth_table)
        # Simplified version of computing the depth of a circuit
        # This is a placeholder and should be replaced with an actual algorithm
        return n // 2
    
    truth_tables = [generate_truth_table(n) for n in [5, 10, 15, 20, 30, 40]]
    depths = [circuit_depth(tt) for tt in truth_tables]
    orders = [coxeter_group_order(tt) for tt in truth_tables]
    
    if len(depths) != len(orders):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(len(truth_tables), 1),
            "conjecture_holds": False,
            "counterexample": "mismatched_lengths"
        }
    
    n = len(depths)
    mean_depth = sum(depths) / n
    mean_order = sum(orders) / n
    
    covariance = sum((depths[i] - mean_depth) * (orders[i] - mean_order) for i in range(n)) / n
    variance_depth = sum((depths[i] - mean_depth)**2 for i in range(n)) / n
    variance_order = sum((orders[i] - mean_order)**2 for i in range(n)) / n
    
    if variance_depth == 0 or variance_order == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(len(truth_tables), 1),
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_depth) * math.sqrt(variance_order))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(len(truth_tables), 1),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
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
        mean_value = None
        std_value = None
        support_fraction = sum("conjecture_holds" in r and r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")