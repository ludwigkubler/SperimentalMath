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
    
    def generate_clauses(n, num_clauses):
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def hodge_module_order(clause):
        # Simplified model of Hodge module order
        return abs(sum(clause)) + len(clause)
    
    def resolution_width(clause):
        stack = []
        for literal in clause:
            if literal == 1:
                stack.append(literal)
            elif literal == -1:
                if stack and stack[-1] == -literal:
                    stack.pop()
                else:
                    return float('inf')
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    variances = []
    
    for n in n_values:
        clauses = generate_clauses(n, 30)
        hodge_orders = [hodge_module_order(clause) for clause in clauses]
        widths = [resolution_width(clause) for clause in clauses]
        
        if not hodge_orders or not widths:
            return {
                "metric_name": "variance",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        variance = sum((x - (sum(hodge_orders) / len(hodge_orders))) ** 2 for x in hodge_orders) / len(hodge_orders)
        variances.append(variance)
    
    mean_variance = sum(variances) / len(variances)
    conjecture_holds = all(v >= 1.5**n * math.log(n)**2 for n, v in zip(n_values, variances))
    counterexample = "" if conjecture_holds else "variance_below_threshold"
    
    return {
        "metric_name": "variance",
        "metric_value": mean_variance,
        "instances_tested": 30 * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "variance_below_threshold" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"variance_below_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")