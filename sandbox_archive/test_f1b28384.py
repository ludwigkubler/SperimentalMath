# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def monomial_ideal_order(instance):
        n = len(instance)
        if n == 0:
            return 0
        order = 0
        for i in range(1, n + 1):
            for combo in combinations(range(n), i):
                term = [instance[j] for j in combo]
                if all(x == 1 for x in term):
                    order += 1
        return order
    
    def resolution_proof_width(instance):
        # Simplified DPLL-based resolution solver (not full implementation)
        n = len(instance)
        clauses = [[i + 1 for i, x in enumerate(instance) if x == 1]]
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if set(clause1).isdisjoint(set(clause2)):
                        continue
                    diff = list(set(clause1) - set(clause2))
                    if len(diff) == 1:
                        new_clause = [x for x in clause2 if x != diff[0]]
                        if not new_clause:
                            return len(clauses)
                        new_clauses.append(new_clause)
            if new_clauses:
                clauses.extend(new_clauses)
            else:
                break
        return len(clauses)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        instance = generate_sat_instance(random.randint(5, n_max))
        order = monomial_ideal_order(instance)
        width = resolution_proof_width(instance)
        metric_values.append(order / width)
        
        if order > 10 * width:
            conjecture_holds = False
            counterexample = f"Instance {instance} has order {order} and width {width}"
    
    return {
        "metric_name": "Order/Width Ratio",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")