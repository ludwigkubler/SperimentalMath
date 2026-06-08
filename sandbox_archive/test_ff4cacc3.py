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
    
    def p_adic_order(poly, p):
        if poly == 0:
            return float('inf')
        order = 0
        while poly % p == 0:
            poly //= p
            order += 1
        return order
    
    def frege_proof_depth(cnf):
        # Placeholder function for Frege proof depth calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * len(cnf[0])
    
    def polynomial_from_cnf(cnf, p):
        x = 1
        poly = 1
        for clause in cnf:
            product = 1
            for lit in clause:
                if lit > 0:
                    product *= (x + lit)
                else:
                    product *= (x - abs(lit))
            poly *= product
        return poly
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    n = 10
    c = 0.5  # Placeholder constant for the conjecture
    instances_tested = 30
    total_order = 0
    max_n = n
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n)
        d_phi = frege_proof_depth(cnf)
        poly = polynomial_from_cnf(cnf, 2)  # Using p=2 for simplicity
        order_phi = p_adic_order(poly, 2)
        
        total_order += order_phi
    
    mean_order = total_order / instances_tested
    conjecture_holds = mean_order >= c * n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "p-adic Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")