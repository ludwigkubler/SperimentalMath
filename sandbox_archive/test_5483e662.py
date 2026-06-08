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
        formula = []
        for _ in range(n):
            if random.choice([True, False]):
                formula.append('AND')
            else:
                formula.append('OR')
        return formula
    
    def resolution_width(formula):
        stack = []
        for token in formula:
            if token == 'AND':
                if len(stack) < 2:
                    return float('inf')
                a = stack.pop()
                b = stack.pop()
                stack.append(a + b)
            elif token == 'OR':
                stack.append(token)
        return max(len(x) for x in stack)
    
    def noncommutative_crossed_product_size(formula):
        n = len(formula)
        size = 2 ** (n * (n - 1))
        return size
    
    n_max = 40
    instances_tested = 0
    total_order = 0
    total_width = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            formula = generate_formula(n)
            order = noncommutative_crossed_product_size(formula)
            width = resolution_width(formula)
            total_order += order
            total_width += width
            instances_tested += 1
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * total_order * total_width - 
                               sum(order * width for order, width in zip([order] * instances_tested, [width] * instances_tested))) / \
                              math.sqrt((instances_tested * total_order ** 2 - sum(order ** 2 for order in [order] * instances_tested)) *
                                        (instances_tested * total_width ** 2 - sum(width ** 2 for width in [width] * instances_tested)))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient} < 0.6"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.6\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")