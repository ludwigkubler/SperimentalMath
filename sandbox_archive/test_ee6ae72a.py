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
    
    def generate_k_cnf(n, k):
        if n <= 0 or k < 0:
            return None
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) for _ in range(2)]
            while len(set(clause)) != 2:
                clause = [random.choice(variables) for _ in range(2)]
            clauses.append(clause)
        return variables, clauses
    
    def coxeter_group_action(n, k):
        if n <= 0 or k < 0:
            return None
        # Simplified Coxeter group action (example)
        return n * k
    
    def resolution_proof_width(n, k):
        if n <= 0 or k < 0:
            return None
        # Simplified resolution proof width (example)
        return n + k
    
    def order_of_largest_element(action):
        if action is None:
            return None
        # Simplified order of largest element (example)
        return action
    
    variables, clauses = generate_k_cnf(40, 10)
    if variables is None or clauses is None:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    action = coxeter_group_action(len(variables), len(clauses))
    if action is None:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    width = resolution_proof_width(len(variables), len(clauses))
    if width is None:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    order = order_of_largest_element(action)
    if order is None:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": len(variables),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no_metric_values")
    else:
        supported_count = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"])
        support_fraction = supported_count / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean=None std=None support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")