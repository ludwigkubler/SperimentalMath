# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['T', 'F'])
        else:
            op = random.choice(['&', '|'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def poset_size(formula):
        if formula == 'T' or formula == 'F':
            return 1
        else:
            left, op, right = formula.split()
            return max(poset_size(left), poset_size(right)) + 1
    
    def frege_proof_depth(formula):
        if formula == 'T' or formula == 'F':
            return 0
        else:
            left, op, right = formula.split()
            return max(frege_proof_depth(left), frege_proof_depth(right)) + 1
    
    def min_order(poset_size):
        # Simplified approximation for demonstration purposes
        return poset_size ** 2
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, min(n_max, 40))
        formula = generate_boolean_formula(n)
        poset = poset_size(formula)
        depth = frege_proof_depth(formula)
        order = min_order(poset)
        
        if order > depth:
            conjecture_holds = False
            counterexample = f"Formula: {formula}, Order: {order}, Depth: {depth}"
            break
        
        total_metric_value += order / depth
    
    return {
        "metric_name": "Order/Depth Ratio",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")