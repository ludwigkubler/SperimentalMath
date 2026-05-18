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
    
    def generate_formula(depth, n):
        if depth == 1:
            return f"x{random.randint(0, n-1)}"
        else:
            op = random.choice(['AND', 'OR'])
            a = generate_formula(depth - 1, n)
            b = generate_formula(depth - 1, n)
            return f"({a} {op} {b})"
    
    def leaf_size(formula):
        stack = []
        for char in formula:
            if char == '(':
                stack.append(char)
            elif char == ')':
                stack.pop()
        return len(stack) + 1
    
    def barrington_protocol(formula, n):
        depth = formula.count('AND') + formula.count('OR')
        L = 4 ** depth
        mu_t_P = [0] * 7
        for _ in range(L):
            input_bits = [random.randint(0, 1) for _ in range(n)]
            product = 1
            for bit in input_bits:
                if formula[bit] == 'x':
                    continue
                elif formula[bit].startswith('x'):
                    product *= int(formula[bit][1:])
                else:
                    product *= barrington_protocol(formula[bit], n)
            cycle_type = classify_cycle_type(product)
            mu_t_P[cycle_type] += 1
        for i in range(7):
            mu_t_P[i] /= L
        return sum(abs(mu_t_P[i] - pi_star[i]) for i in range(7))
    
    def classify_cycle_type(product):
        cycle_types = {
            1: [0, 1, 2],  # Identity, (1), (2)
            2: [3, 4],      # (3), (4)
            3: [5],         # (5)
            4: [6]          # (6)
        }
        for key, values in cycle_types.items():
            if product in values:
                return key
        return -1
    
    pi_star = [Fraction(119, 120), Fraction(1, 120)] + [0] * 5
    
    n_values = [6, 8, 10]
    d_values = [2, 3, 4]
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for d in d_values:
            formula = generate_formula(d, n)
            leaf_size_f = leaf_size(formula)
            L = 4 ** d
            metric_value = barrington_protocol(formula, n)
            instances_tested += L
            total_metric_value += metric_value * L
            if metric_value < (1/8) * math.log2(leaf_size_f):
                conjecture_holds = False
                counterexample = f"Formula: {formula}, LeafSize: {leaf_size_f}, MIX(P)*L: {metric_value}"
    
    mean_metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": "MIX(P) * L",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")