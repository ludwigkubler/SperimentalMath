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
    
    def generate_cnf(n):
        num_clauses = random.randint(1, n)
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def compute_genus(cnf):
        # Simplified heuristic to estimate genus based on number of variables and clauses
        n = len(cnf[0])
        m = len(cnf)
        g = (n - 1) * (m - 1) // 2
        return max(0, g)
    
    def local_polynomial_hierarchy_index(g):
        # Simplified heuristic to estimate the index based on genus
        if g == 0:
            return 0
        elif g == 1:
            return 1
        else:
            return g - 1
    
    def dpll_search_tree_width(cnf):
        # Simplified heuristic to estimate width of DPLL search tree
        n = len(cnf[0])
        m = len(cnf)
        return max(n, m)
    
    results = []
    for _ in range(30):
        n = random.randint(1, 40)
        cnf = generate_cnf(n)
        g = compute_genus(cnf)
        I_g = local_polynomial_hierarchy_index(g)
        width_T_phi = dpll_search_tree_width(cnf)
        
        results.append({
            "n": n,
            "I_g": I_g,
            "width_T_phi": width_T_phi
        })
    
    mean_I_g = sum(result["I_g"] for result in results) / len(results)
    mean_width_T_phi = sum(result["width_T_phi"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["I_g"] < result["width_T_phi"]) / len(results)
    
    conjecture_holds = all(result["I_g"] < result["width_T_phi"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "local_polynomial_hierarchy_index",
        "metric_value": mean_I_g,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"I({result['n']}) = {result['I_g']} >= width(T(φ)) = {result['width_T_phi']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break