# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

# Function to generate random Boolean formulas
def generate_formula(n):
    if n == 1:
        return random.choice(['T', 'F'])
    else:
        op = random.choice(['&', '|'])
        left = generate_formula(n - 1)
        right = generate_formula(n - 1)
        return f"({left} {op} {right})"

# Function to calculate the Frege proof depth
def frege_proof_depth(formula):
    if formula == 'T' or formula == 'F':
        return 0
    else:
        left, op, right = formula[1:-1].split()
        return max(frege_proof_depth(left), frege_proof_depth(right)) + 1

# Function to calculate the minimal order of a monoid in the category of endofunctors of the poset [φ]
def min_order(formula):
    if formula == 'T':
        return 1
    elif formula == 'F':
        return 0
    else:
        left, op, right = formula[1:-1].split()
        if op == '&':
            return min(min_order(left), min_order(right))
        elif op == '|':
            return max(min_order(left), min_order(right))

# Function to calculate the size of the poset [φ]
def poset_size(formula):
    if formula == 'T' or formula == 'F':
        return 1
    else:
        left, _, right = formula[1:-1].split()
        return max(poset_size(left), poset_size(right)) + 1

# Function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    metric_value = 0.0
    instances_tested = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        formula = generate_formula(n)
        f_depth = frege_proof_depth(formula)
        monoid_order = min_order(formula)
        
        if n > n_max:
            n_max = n
        
        metric_value += monoid_order / f_depth
        instances_tested += 1
    
    conjecture_holds = True
    counterexample = ""
    
    if instances_tested == 30:
        mean_metric_value = metric_value / instances_tested
        std_metric_value = 0.0
        
        for _ in range(29):
            n = random.randint(5, 40)
            formula = generate_formula(n)
            f_depth = frege_proof_depth(formula)
            monoid_order = min_order(formula)
            
            if n > n_max:
                n_max = n
            
            std_metric_value += (monoid_order / f_depth - mean_metric_value) ** 2
        
        std_metric_value /= instances_tested
        std_metric_value = math.sqrt(std_metric_value)
        
        support_fraction = 1.0
        
        for _ in range(30):
            n = random.randint(5, 40)
            formula = generate_formula(n)
            f_depth = frege_proof_depth(formula)
            monoid_order = min_order(formula)
            
            if n > n_max:
                n_max = n
            
            if monoid_order / f_depth > support_fraction:
                conjecture_holds = False
                counterexample = f"Formula: {formula}, Monoid Order: {monoid_order}, Frege Depth: {f_depth}"
                break
    
    return {
        "metric_name": "Min Order to Frege Depth Ratio",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main function to run trials with given seeds
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")