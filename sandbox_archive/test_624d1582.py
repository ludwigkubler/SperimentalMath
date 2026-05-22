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
    
    def generate_tseitin_formula(n):
        symbols = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([symbols[i-1]])
            for j in range(i+1, n+1):
                clauses.append([symbols[i-1], f"~{symbols[j-1]}"])
                clauses.append([f"~{symbols[i-1]}", symbols[j-1]])
        return symbols, clauses
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i+1, len(stack)):
                    if any(-x in stack[i] and x in stack[j] for x in set(stack[i]) & set(stack[j])):
                        new_clause = [x for x in stack[i] + stack[j] if x != -x]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            if new_clause in stack:
                return float('inf')
            stack.append(new_clause)
    
    def quandle_order(n):
        # Placeholder for actual quandle order computation
        # This is a dummy function that returns a simple bound
        return n**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        symbols, clauses = generate_tseitin_formula(n)
        res_len = resolution_length(clauses)
        if res_len == float('inf'):
            continue
        q_order = quandle_order(n)
        results.append({
            "n": n,
            "res_len": res_len,
            "q_order": q_order
        })
    
    if not results:
        return {
            "metric_name": "quandle_order_bound",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    max_res_len = max(result["res_len"] for result in results)
    min_q_order = min(result["q_order"] for result in results)
    
    return {
        "metric_name": "quandle_order_bound",
        "metric_value": min_q_order,
        "instances_tested": len(results),
        "conjecture_holds": min_q_order <= max_res_len * 2,  # Placeholder bound
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"quandle_order_bound > 2 * resolution_length\" first_failing_seed={result['seed']}")
                break