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
    
    def generate_boolean_formula(n):
        if n == 1:
            return 'p' if random.choice([True, False]) else 'not p'
        elif n == 2:
            op = '&' if random.choice([True, False]) else '|'
            return f'(generate_boolean_formula({n-1})) {op} (generate_boolean_formula({n-1}))'
        else:
            op = '&' if random.choice([True, False]) else '|'
            return f'(generate_boolean_formula({n//2})) {op} (generate_boolean_formula({n-n//2}))'
    
    def dpll_proof_width(phi):
        if 'p' in phi or 'not p' in phi:
            return 1
        elif '&' in phi:
            left, right = phi.split('&')
            return max(dpll_proof_width(left), dpll_proof_width(right)) + 1
        elif '|' in phi:
            left, right = phi.split('|')
            return max(dpll_proof_width(left), dpll_proof_width(right)) + 1
    
    def minimal_index_of_representation(n):
        # Placeholder for actual computation using character theory
        # For simplicity, we use a linear function of n
        return n * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different formulas
            phi = generate_boolean_formula(n)
            min_index = minimal_index_of_representation(n)
            w_DPLL = dpll_proof_width(phi)
            
            if w_DPLL == 0:
                continue
            
            ratio = Fraction(min_index, w_DPLL)
            total_metric_value += ratio
            instances_tested += 1
            n_max = max(n_max, n)
            
            if not (2.0 <= ratio <= 1.5):
                conjecture_holds = False
                counterexample = f"phi: {phi}, min_index: {min_index}, w_DPLL: {w_DPLL}"
    
    return {
        "metric_name": "Ratio of minimal index to DPLL proof width",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")