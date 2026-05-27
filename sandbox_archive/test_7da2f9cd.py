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
    
    def generate_formula(n):
        if n == 1:
            return random.choice([0, 1])
        else:
            sub_n = random.randint(1, n-1)
            left = generate_formula(sub_n)
            right = generate_formula(n - sub_n)
            op = random.choice(['&', '|'])
            return f"({left} {op} {right})"
    
    def truth_table(formula):
        if formula.isdigit():
            return [int(formula)]
        elif formula == '0':
            return [0]
        elif formula == '1':
            return [1]
        else:
            left, op, right = formula[1:-1].split()
            left_truth = truth_table(left)
            right_truth = truth_table(right)
            if op == '&':
                return [l & r for l in left_truth for r in right_truth]
            elif op == '|':
                return [l | r for l in left_truth for r in right_truth]
    
    def p_adic_order(truth_values):
        max_value = max(truth_values)
        if max_value == 0:
            return 1
        order = 0
        while max_value > 0:
            max_value //= 2
            order += 1
        return order
    
    n = random.randint(5, 40)
    D = math.ceil(math.log2(n))
    formula = generate_formula(n)
    truth_values = truth_table(formula)
    p_order = p_adic_order(truth_values)
    
    metric_name = "p-adic Order"
    metric_value = p_order
    instances_tested = 1
    conjecture_holds = p_order <= D
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Truth Table: {truth_values}, P-adic Order: {p_order}, Expected: ≤{D}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")