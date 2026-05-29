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
from math import log, ceil

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['&', '|', '^'])
            left = generate_boolean_formula(random.randint(1, n-1))
            right = generate_boolean_formula(n - len(left.split('&')) - len(left.split('|')) - len(left.split('^')))
            return f'({left} {op} {right})'
    
    def dpll_tree_height(formula):
        if formula in ['True', 'False']:
            return 0
        else:
            op = formula[1]
            left, right = formula[2:-1].split(' ', 1)
            return max(dpll_tree_height(left), dpll_tree_height(right)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            formula = generate_boolean_formula(n)
            height = dpll_tree_height(formula)
            k = (height - log(n, 2)) / log(n, 2)
            if k < 0 or not conjecture_holds:
                conjecture_holds = False
                counterexample = f"Formula: {formula}, Height: {height}, k: {k}"
                break
            total_metric_value += height
            instances_tested += 1
    
    return {
        "metric_name": "DPLL Tree Height",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")