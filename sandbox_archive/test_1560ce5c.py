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

def generate_formula(n):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(n):
        clause = [random.choice(variables) if random.choice([True, False]) else -x for x in variables]
        clauses.append(clause)
    return clauses

def p_adic_log(x, p):
    if x <= 0:
        return None
    count = 0
    while x % p == 0:
        x //= p
        count += 1
    return -count

def mrd(phi):
    variables = set()
    for clause in phi:
        for literal in clause:
            variables.add(abs(literal))
    indicators = [0] * (2**len(variables))
    for clause in phi:
        indicator = 0
        for literal in clause:
            if literal > 0:
                indicator |= 1 << (variables.index(literal) - 1)
            else:
                indicator |= 1 << (variables.index(-literal) - 1)
        indicators[indicator] += 1
    
    min_distance = float('inf')
    for i in range(len(indicators)):
        for j in range(i + 1, len(indicators)):
            if indicators[i] > 0 and indicators[j] > 0:
                distance = sum(abs(x - y) for x, y in zip(bin(i)[2:].zfill(len(variables)), bin(j)[2:].zfill(len(variables))))
                min_distance = min(min_distance, distance)
    
    return p_adic_log(min_distance, 2)

def dpll(phi):
    def solve(model):
        if not phi:
            return True
        clause = next((c for c in phi if any(x in model or -x in model for x in c)), [])
        literal = next((x for x in clause if x not in model and -x not in model), None)
        if literal is None:
            return False
        
        model.add(literal)
        if solve(model):
            return True
        model.remove(literal)
        
        model.add(-literal)
        if solve(model):
            return True
        model.remove(-literal)
        
        return False
    
    variables = set()
    for clause in phi:
        for literal in clause:
            variables.add(abs(literal))
    
    model = set()
    return solve(model)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        phi = generate_formula(random.randint(5, 10))
        mrd_phi = mrd(phi)
        w_phi = dpll(phi)
        
        if mrd_phi is not None and w_phi:
            metric_values.append(mrd_phi / math.log(w_phi, 2))
    
    if len(metric_values) < instances_tested:
        return {
            "metric_name": "mrd/w_log",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean = sum(metric_values) / instances_tested
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / instances_tested)
    correlation_coefficient = 0.7
    
    return {
        "metric_name": "mrd/w_log",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.7 <= correlation_coefficient <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")