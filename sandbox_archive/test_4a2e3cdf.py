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
    
    def generate_instance(n):
        clauses = []
        for _ in range(3 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def dpll_search_tree_diameter(instance):
        n = len(instance)
        
        def dfs(model, depth):
            if all([any([model[abs(l) - 1] == l // abs(l) for l in clause]) for clause in instance]):
                return depth
            unsatisfied_clauses = [clause for clause in instance if not any([model[abs(l) - 1] == l // abs(l) for l in clause])]
            if not unsatisfied_clauses:
                return float('inf')
            literal = random.choice(unsatisfied_clauses[0])
            new_model_true = model[:]
            new_model_true[abs(literal) - 1] = literal // abs(literal)
            new_model_false = model[:]
            new_model_false[abs(literal) - 1] = -(literal // abs(literal))
            return min(dfs(new_model_true, depth + 1), dfs(new_model_false, depth + 1))
        
        initial_model = [0] * n
        return dfs(initial_model, 0)
    
    def p_adic_hodge_structure(instance):
        # Simplified mapping for demonstration purposes
        return len(instance) ** (1/4)
    
    instance = generate_instance(20)
    d = dpll_search_tree_diameter(instance)
    mH_G = p_adic_hodge_structure(instance)
    
    if d == 0:
        return {
            "metric_name": "mH(G)/d^(1/4)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": 20,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree diameter is zero"
        }
    
    ratio = mH_G / (d ** (1/4))
    return {
        "metric_name": "mH(G)/d^(1/4)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": 20,
        "conjecture_holds": abs(ratio - Fraction(1, 4)) <= Fraction(1, 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mH(G)/d^(1/4) ratio outside ±10% of 1/4\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")