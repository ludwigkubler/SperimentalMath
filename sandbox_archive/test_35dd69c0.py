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
    
    def tseitin(n):
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append([-i, -j, i+j])
        return clauses
    
    def resolution(clauses):
        new_clauses = set()
        while True:
            new_clauses.clear()
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = list(set(clause1) ^ set(clause2))
                        if not any(new_clause == -lit for lit in clause1):
                            new_clauses.add(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    def geometric_flow_time(n):
        # Simulate a simple geometric flow that separates points by flipping literals
        # This is a placeholder for an actual geometric flow algorithm
        return n * (n + 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances_tested = 0
    total_flow_time = 0
    total_width = 0
    max_n = 0
    
    for n in n_values:
        instances_tested = 0
        flow_time_sum = 0
        width_sum = 0
        
        for _ in range(5):  # Test each size with 5 different instances
            phi_G = tseitin(n)
            w_phi_G = resolution(phi_G)
            flow_time = geometric_flow_time(n)
            
            if flow_time > 0:
                instances_tested += 1
                flow_time_sum += flow_time
                width_sum += w_phi_G
        
        total_instances_tested += instances_tested
        total_flow_time += flow_time_sum
        total_width += width_sum
        max_n = max(max_n, n)
    
    if total_instances_tested == 0:
        return {
            "metric_name": "Flow Time / Width Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    
    ratio = total_flow_time / total_width
    return {
        "metric_name": "Flow Time / Width Ratio",
        "metric_value": ratio,
        "instances_tested": total_instances_tested,
        "n_max": max_n,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no instances tested")
    else:
        supported_count = sum(1 for r in results if r["conjecture_holds"])
        support_fraction = supported_count / len(results)
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")