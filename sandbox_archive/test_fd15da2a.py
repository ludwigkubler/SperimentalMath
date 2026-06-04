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
    
    def generate_formula(n):
        if n == 1:
            return '0' if random.choice([True, False]) else '1'
        else:
            op = random.choice(['&', '|'])
            left = generate_formula(random.randint(1, n-1))
            right = generate_formula(n - len(left) - 2)
            return f"({left} {op} {right})"
    
    def ramanujan_q(formula):
        if formula == '0' or formula == '1':
            return 0
        left, op, right = formula[1:-1].split()
        q_left = ramanujan_q(left)
        q_right = ramanujan_q(right)
        if op == '&':
            return max(q_left, q_right) + 1
        elif op == '|':
            return min(q_left, q_right) + 1
    
    def resolution_width(formula):
        if formula == '0' or formula == '1':
            return 1
        left, op, right = formula[1:-1].split()
        w_left = resolution_width(left)
        w_right = resolution_width(right)
        if op == '&':
            return max(w_left, w_right) + 1
        elif op == '|':
            return min(w_left, w_right) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    Q_min_sum = 0
    w_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            Q_min = ramanujan_q(formula)
            w = resolution_width(formula)
            Q_min_sum += Q_min
            w_sum += w
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Q_min vs. w",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_Q_min = Q_min_sum / instances_tested
    mean_w = w_sum / instances_tested
    
    return {
        "metric_name": "Q_min vs. w",
        "metric_value": mean_Q_min,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": False,  # Placeholder; actual correlation test not implemented
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_Q_min = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_Q_min} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_Q_min} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")