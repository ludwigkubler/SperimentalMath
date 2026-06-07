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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(f, n):
        literals = {i: f[i] for i in range(n)}
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
        return clauses
    
    def resolution_proof_depth(clauses):
        stack = [clauses]
        while stack:
            clause = stack.pop()
            if not clause:
                continue
            literal = random.choice(clause)
            new_clauses = []
            for c in stack:
                if literal in c:
                    new_clauses.append([x for x in c if x != literal])
                elif -literal in c:
                    new_clauses.append([x for x in c if x != -literal])
            stack.extend(new_clauses)
        return len(stack)
    
    def algebraic_degree(f, n):
        degree = 0
        for i in range(n):
            if f[i] == 1:
                degree += 1
        return degree
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_boolean_function(n)
        clauses = tseitin_formula(f, n)
        depth = resolution_proof_depth(clauses)
        degree = algebraic_degree(f, n)
        results.append((degree, depth))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    degrees, depths = zip(*results)
    mean_degree = sum(degrees) / len(degrees)
    mean_depth = sum(depths) / len(depths)
    correlation = (sum((d - mean_degree) * (p - mean_depth) for d, p in results) /
                   math.sqrt(sum((d - mean_degree)**2 for d in degrees) *
                             sum((p - mean_depth)**2 for p in depths)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation > 0.7 and all(c >= 0.5 for c in [correlation]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")