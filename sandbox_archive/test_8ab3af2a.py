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
    
    def smallest_normal_subgroup_order(order):
        if order <= 1:
            return 0
        for i in range(2, int(math.sqrt(order)) + 1):
            if order % i == 0:
                return i
        return order
    
    def generate_boolean_formula(n):
        variables = list(range(n))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def galois_group_order(formula):
        # Simplified version of the Galois group order calculation
        # This is a placeholder and should be replaced with actual computation
        return len(formula) ** 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_boolean_formula(n)
        order = galois_group_order(formula)
        subgroup_order = smallest_normal_subgroup_order(order)
        
        if subgroup_order < math.log(n, 2) or subgroup_order > (math.log(n, 2)) ** 2:
            return {
                "metric_name": "subgroup_order",
                "metric_value": subgroup_order,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Formula with n={n} has subgroup order {subgroup_order}"
            }
        
        results.append(subgroup_order)
    
    return {
        "metric_name": "subgroup_order",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= math.log(40, 2) and r <= (math.log(40, 2)) ** 2) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < math.log(5, 2) or r > (math.log(5, 2)) ** 2 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < math.log(5, 2) or r > (math.log(5, 2)) ** 2))]
        print(f"RESULT: FALSIFIED counterexample='n=5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")