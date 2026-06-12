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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def dpll(instance):
        if not instance:
            return 1
        var = instance[0]
        pos_clauses = [cl for cl in clauses if var in cl]
        neg_clauses = [cl for cl in clauses if -var in cl]
        if any(not any(lit in assignment for lit in cl) for cl in pos_clauses):
            return 0
        if any(all(lit not in assignment for lit in cl) for cl in neg_clauses):
            return 0
        assignment[var] = True
        result_pos = dpll(instance[1:])
        del assignment[var]
        assignment[-var] = True
        result_neg = dpll(instance[1:])
        del assignment[-var]
        return max(result_pos, result_neg)
    
    def hodge_arc_length(n):
        # Simplified approximation for demonstration purposes
        return n
    
    def pearson_correlation(data_x, data_y):
        if len(data_x) != len(data_y):
            raise ValueError("Data sets must have the same length")
        mean_x = sum(data_x) / len(data_x)
        mean_y = sum(data_y) / len(data_y)
        cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(data_x, data_y)) / len(data_x)
        std_x = math.sqrt(sum((x - mean_x) ** 2 for x in data_x) / len(data_x))
        std_y = math.sqrt(sum((y - mean_y) ** 2 for y in data_y) / len(data_y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    instances_tested = 0
    
    for n in n_values:
        instance = generate_instance(n)
        clauses = []
        for i in range(1 << n):
            clause = [random.choice([-i-1, i+1]) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        
        assignment = {}
        width = dpll(instance)
        arc_length = hodge_arc_length(n)
        
        results.append({
            "metric_name": "Pearson Correlation",
            "metric_value": pearson_correlation([arc_length], [width]),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": ""
        })
        instances_tested += 1
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": instances_tested,
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["metric_value"] > 0.5 and r["p_value"] < 0.1 for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] and r["metric_value"] > 0.5 and r["p_value"] < 0.1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] <= 0.5 or r["p_value"] >= 0.1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")