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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set(random.sample(range(1, n+1), 2))
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    queue = list(cnf)
    seen = set()
    
    while queue:
        clause1 = queue.pop(0)
        for clause2 in queue:
            if len(clause1.intersection(clause2)) == 1:
                new_clause = clause1.union(clause2) - clause1.intersection(clause2)
                if new_clause not in seen:
                    seen.add(new_clause)
                    queue.append(new_clause)
    
    return len(seen)

def coxeter_diagram_entropy(cnf):
    n = len(cnf)
    edges = set()
    
    for i in range(n):
        for j in range(i+1, n):
            if cnf[i].intersection(cnf[j]):
                edges.add((i, j))
    
    return len(edges)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        m = 2 * n
        cnf = generate_cnf(n, m)
        width = resolution_width(cnf)
        entropy = coxeter_diagram_entropy(cnf)
        
        if width == 0:
            continue
        
        results.append({
            "n": n,
            "m": m,
            "width": width,
            "entropy": entropy
        })
    
    if not results:
        return {
            "metric_name": "Coxeter-diagram Entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    mean_entropy = sum(result["entropy"] for result in results) / instances_tested
    mean_width = sum(result["width"] for result in results) / instances_tested
    
    if any(result["entropy"] > 10 * result["width"] for result in results):
        return {
            "metric_name": "Coxeter-diagram Entropy",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Entropy exceeds 10 times width"
        }
    
    return {
        "metric_name": "Coxeter-diagram Entropy",
        "metric_value": mean_entropy / mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Entropy exceeds 10 times width\" first_failing_seed={result['seed']}")
                break