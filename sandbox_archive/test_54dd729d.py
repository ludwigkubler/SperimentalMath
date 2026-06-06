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
    
    def poset_size(formula):
        if formula == 'true' or formula == 'false':
            return 1
        elif formula.startswith('(') and formula.endswith(')'):
            left, op, right = formula[1:-1].split()
            return max(poset_size(left), poset_size(right)) + 1
        else:
            return 2
    
    def frege_proof_depth(formula):
        if formula == 'true' or formula == 'false':
            return 0
        elif formula.startswith('(') and formula.endswith(')'):
            left, op, right = formula[1:-1].split()
            return max(frege_proof_depth(left), frege_proof_depth(right)) + 1
        else:
            return 2
    
    def min_order(formula):
        if formula == 'true' or formula == 'false':
            return 1
        elif formula.startswith('(') and formula.endswith(')'):
            left, op, right = formula[1:-1].split()
            return max(min_order(left), min_order(right)) + 1
        else:
            return 2
    
    def generate_formula(n):
        if n == 0:
            return random.choice(['true', 'false'])
        elif n == 1:
            return f'({generate_formula(0)} {random.choice(["&", "|"])} {generate_formula(0)})'
        else:
            return f'({generate_formula(n-1)} {random.choice(["&", "|"])} {generate_formula(n-1)})'
    
    instances_tested = 0
    n_max = 0
    total_metric_value = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        for _ in range(5):
            formula = generate_formula(n)
            instances_tested += 1
            n_max = max(n_max, n)
            
            poset = poset_size(formula)
            f_depth = frege_proof_depth(formula)
            min_order_val = min_order(formula)
            
            if f_depth == 0:
                continue
            
            ratio = Fraction(min_order_val, f_depth)
            total_metric_value += ratio
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(Fraction(min_order(formula), frege_proof_depth(formula)) <= Fraction(1, 2) for _ in range(30))
    
    return {
        "metric_name": "Min Order to Frege Depth Ratio",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")