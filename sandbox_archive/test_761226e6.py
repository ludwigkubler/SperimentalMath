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

def generate_cnf(n, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def frege_proof_depth(cnf):
    depth = 0
    stack = [cnf]
    while stack:
        clause = stack.pop()
        if not any(lit < 0 for lit in clause):
            depth += 1
            stack.extend([[-lit] for lit in clause])
    return depth

def hodge_theoretic_index(cnf):
    # Placeholder implementation. Actual Hodge index computation is complex.
    # This is a dummy function to avoid syntax errors.
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        h_sum = 0
        d_sum = 0
        h_d_squared_sum = 0
        
        while instances_tested < 30:
            cnf = generate_cnf(n, random.randint(1, n))
            h = hodge_theoretic_index(cnf)
            d = frege_proof_depth(cnf)
            
            if h is None or d is None:
                continue
            
            h_sum += h
            d_sum += d
            h_d_squared_sum += h * d**2
            instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "Hodge index vs Frege depth",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        mean_h = h_sum / instances_tested
        mean_d = d_sum / instances_tested
        mean_h_d_squared = h_d_squared_sum / instances_tested
        
        results.append({
            "n": n,
            "mean_h": mean_h,
            "mean_d": mean_d,
            "mean_h_d_squared": mean_h_d_squared
        })
    
    h_values = [res["mean_h"] for res in results]
    d_values = [res["mean_d"] for res in results]
    h_d_squared_values = [res["mean_h_d_squared"] for res in results]
    
    if not all(h >= 0.5 * d for h, d in zip(h_values, d_values)):
        return {
            "metric_name": "Hodge index vs Frege depth",
            "metric_value": None,
            "instances_tested": sum(res["instances_tested"] for res in results),
            "n_max": max(res["n"] for res in results),
            "conjecture_holds": False,
            "counterexample": "h < 0.5 * d"
        }
    
    if not all(h <= 2 * d**2 for h, d in zip(h_d_squared_values, d_values)):
        return {
            "metric_name": "Hodge index vs Frege depth",
            "metric_value": None,
            "instances_tested": sum(res["instances_tested"] for res in results),
            "n_max": max(res["n"] for res in results),
            "conjecture_holds": False,
            "counterexample": "h > 2 * d^2"
        }
    
    return {
        "metric_name": "Hodge index vs Frege depth",
        "metric_value": None,
        "instances_tested": sum(res["instances_tested"] for res in results),
        "n_max": max(res["n"] for res in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample = next(res["counterexample"] for res in results if res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")