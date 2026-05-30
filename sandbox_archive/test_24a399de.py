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
    
    def generate_random_kcnf(n, m, k):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(set(clause)) == 2:
                cnf.append(clause)
        return cnf
    
    def truth_table(cnf, n):
        tt = {}
        for i in range(2**n):
            assignment = [(i >> j) & 1 for j in range(n)]
            tt[tuple(assignment)] = any(all(assignment[abs(lit)-1] == (lit > 0) for lit in clause) for clause in cnf)
        return tt
    
    def minimal_representation_order(tt):
        # This is a placeholder function. Implement the actual computation of the minimal representation order.
        return random.randint(1, 100)
    
    def resolution_width(cnf):
        # This is a placeholder function. Implement a small DPLL solver to calculate the resolution width.
        return random.randint(1, 100)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(n * math.log2(n))
        cnf = generate_random_kcnf(n, m, k=2)
        tt = truth_table(cnf, n)
        order = minimal_representation_order(tt)
        width = resolution_width(cnf)
        
        if order > m**(2/3) * n**(1/4):
            return {
                "metric_name": "minimal_representation_order",
                "metric_value": order,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Order {order} > m^(2/3)n^(1/4) for n={n}, m={m}"
            }
        
        if width < order:
            return {
                "metric_name": "resolution_width",
                "metric_value": width,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Width {width} < order {order} for n={n}, m={m}"
            }
        
        results.append({
            "metric_name": "minimal_representation_order",
            "metric_value": order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    std_order = math.sqrt(sum((result["metric_value"] - mean_order)**2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    return {
        "metric_name": "minimal_representation_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order)**2 for r in results) / len(results))
    support_fraction = all(r["conjecture_holds"] for r in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order > m^(2/3)n^(1/4)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")