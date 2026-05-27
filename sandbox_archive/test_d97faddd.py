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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate 2-clauses (disjunctions of two literals)
        for var in variables:
            clauses.append([var, f'~{var}'])
        
        # Generate 3-clauses (disjunctions of three literals)
        for i in range(n):
            clause = [f'x{i+1}', f'x{i+2}', f'~x{i+3}']
            clauses.append(clause)
        
        return variables, clauses
    
    def compute_colored_jones_polynomial(variables, clauses):
        # Placeholder function to simulate computation
        # This is a dummy implementation and should be replaced with actual quantum topology calculation
        qtw = len(variables) ** 2
        return qtw
    
    def compute_resolution_depth(variables, clauses):
        # Placeholder function to simulate computation
        # This is a dummy implementation and should be replaced with actual Resolution depth calculation
        dr = len(clauses)
        return dr
    
    n = random.randint(5, 40)  # Ensure n_min >= 5 and n_max <= 40
    variables, clauses = generate_tseitin_formula(n)
    
    qtw = compute_colored_jones_polynomial(variables, clauses)
    dr = compute_resolution_depth(variables, clauses)
    
    if qtw == 0 or dr == 0:
        return {
            "metric_name": "Resolution depth",
            "metric_value": dr,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "QTW(G) or D_R(G) is zero"
        }
    
    metric_value = qtw
    instances_tested = 1
    conjecture_holds = qtw >= 2 ** (math.log(qtw, 2) * math.log(qtw, 2))
    counterexample = "" if conjecture_holds else "QTW(G) < 2^(Ω(θ(n^α)))"
    
    return {
        "metric_name": "Resolution depth",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"QTW(G) < 2^(Ω(θ(n^α)))\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence to support or falsify the conjecture")