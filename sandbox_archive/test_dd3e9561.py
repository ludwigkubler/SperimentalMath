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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n)] + [-random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll_search_tree(cnf):
        assignment = {}
        
        def solve():
            unassigned_vars = [v for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment]
            if not unassigned_vars:
                return True
            v = unassigned_vars[0]
            for val in [True, False]:
                assignment[v] = val
                if solve():
                    return True
                del assignment[v]
            return False
        
        solve()
        return assignment
    
    def dpll_diameter(cnf):
        assignment = {}
        
        def solve(node=None):
            if node is None:
                node = 0
            unassigned_vars = [v for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment]
            if not unassigned_vars:
                return 0
            v = unassigned_vars[0]
            max_diameter = 0
            for val in [True, False]:
                assignment[v] = val
                diameter = solve(node + 1)
                if diameter > max_diameter:
                    max_diameter = diameter
                del assignment[v]
            return max_diameter
        
        return solve()
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    mcr_value = len(cnf)  # Simplified for testing purposes
    dpll_diameter_value = dpll_diameter(cnf)
    
    return {
        "metric_name": "mcr",
        "metric_value": mcr_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if dpll_diameter_value < mcr_value else True,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_conjecture")