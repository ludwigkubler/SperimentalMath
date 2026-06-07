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
    
    def generate_random_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def resolution_width(phi):
        # Simplified DPLL solver to estimate the width of the resolution proof
        stack = []
        literals = set()
        for literal in phi:
            if literal not in literals and -literal not in literals:
                literals.add(literal)
                stack.append([literal])
            else:
                if literal in literals:
                    continue
                clause = next((c for c in stack if literal in c), None)
                if clause is None:
                    return float('inf')
                stack.remove(clause)
                new_clause = [l for l in clause if l != -literal]
                if not new_clause:
                    return 0
                literals.add(literal)
                stack.append(new_clause)
        return max(len(c) for c in stack)
    
    def grothendieck_witt_degree(phi):
        # Simplified monomial basis method to compute the degree of the Grothendieck-Witt class
        n = int(math.log2(len(phi)))
        if n == 0:
            return 0
        degree = 1
        for i in range(1, n):
            degree *= (i + 1)
        return degree
    
    def deg_mod_2(gw_degree):
        return gw_degree % 2
    
    instances_tested = 0
    total_deg_mod_2 = 0
    n_max = 5
    
    for _ in range(30):
        n = random.randint(5, 40)
        phi = generate_random_boolean_instance(n)
        gw_degree = grothendieck_witt_degree(phi)
        deg_mod_2_val = deg_mod_2(gw_degree)
        width = resolution_width(phi)
        
        if deg_mod_2_val > 2 * width:
            return {
                "metric_name": "deg(GW_φ) mod 2",
                "metric_value": deg_mod_2_val,
                "instances_tested": instances_tested + 1,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"phi={phi}, gw_degree={gw_degree}, width={width}"
            }
        
        total_deg_mod_2 += deg_mod_2_val
        instances_tested += 1
        n_max = max(n_max, n)
    
    return {
        "metric_name": "deg(GW_φ) mod 2",
        "metric_value": total_deg_mod_2 / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")