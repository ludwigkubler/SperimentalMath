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
    
    def tropicalize(boolean_function):
        n = int(math.log2(len(boolean_function)))
        t_variety = []
        for i in range(2**n):
            if boolean_function[i] == 1:
                t_variety.append(i)
        return t_variety
    
    def geometric_entropy(t_variety, n):
        total = len(t_variety)
        entropy = -sum(total / (total + 1) * math.log2(total / (total + 1)) for _ in range(total))
        return entropy
    
    def resolution_proof_depth(boolean_function):
        n = int(math.log2(len(boolean_function)))
        clauses = []
        for i in range(n):
            clauses.append([i, i + n])
        depth = 0
        while len(clauses) > 1:
            new_clause = []
            for clause in clauses:
                if len(clause) == 1:
                    new_clause.extend(clause)
                else:
                    new_clause.append(random.choice(clause))
            clauses = new_clause
            depth += 1
        return depth
    
    n_values = [10, 15, 20, 30]
    results = []
    
    for n in n_values:
        boolean_function = generate_boolean_function(n)
        t_variety = tropicalize(boolean_function)
        H_min = geometric_entropy(t_variety, n)
        d_res = resolution_proof_depth(boolean_function)
        results.append({"n": n, "H_min": H_min, "d_res": d_res})
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    H_min_values = [result["H_min"] for result in results]
    d_res_values = [result["d_res"] for result in results]
    
    mean_H_min = sum(H_min_values) / len(H_min_values)
    mean_d_res = sum(d_res_values) / len(d_res_values)
    
    correlation = 0
    if len(H_min_values) > 1 and len(d_res_values) > 1:
        numerator = sum((H_min_values[i] - mean_H_min) * (d_res_values[i] - mean_d_res) for i in range(len(H_min_values)))
        denominator = math.sqrt(sum((H_min_values[i] - mean_H_min)**2 for i in range(len(H_min_values)))) * math.sqrt(sum((d_res_values[i] - mean_d_res)**2 for i in range(len(d_res_values))))
        correlation = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.5 and correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if abs(r["metric_value"]) >= 0.5 and r["metric_value"] >= 0.8) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")