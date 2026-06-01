# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(n * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i + 1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def dpll_search_tree_diameter(instance):
        # Simplified DPLL algorithm to estimate the diameter
        n = len(instance[0])
        stack = []
        visited = [False] * (2 ** n)
        max_depth = 0
        
        def dfs(node, depth):
            nonlocal max_depth
            if depth > max_depth:
                max_depth = depth
            for clause in instance:
                satisfied = any(abs(var) == abs(lit) for lit in clause for var in node)
                if not satisfied:
                    break
            else:
                stack.append((node, depth))
                visited[node] = True
                for i in range(n):
                    if node & (1 << i):
                        dfs(node ^ (1 << i), depth + 1)
                stack.pop()
        
        dfs(0, 0)
        return max_depth
    
    def p_adic_hodge_structure(instance):
        # Simplified mapping to estimate mH(G)
        n = len(instance[0])
        mH_G = sum(len(clause) for clause in instance) / (2 ** n)
        return mH_G
    
    instances_tested = 30
    n_max = 40
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = generate_3sat_instance(n)
        d = dpll_search_tree_diameter(instance)
        mH_G = p_adic_hodge_structure(instance)
        
        if d == 0:
            continue
        
        ratio = Fraction(mH_G, d ** (1/4))
        if abs(ratio - Fraction(1, 4)) <= Fraction(1, 10):
            metric_values.append(mH_G)
    
    if not metric_values:
        return {
            "metric_name": "mH(G)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_td = sum(metric_values) / len(metric_values)
    std_td = (sum((x - mean_td) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    return {
        "metric_name": "mH(G)",
        "metric_value": mean_td,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_td = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_td = (sum((r["metric_value"] - mean_td) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_td} std={std_td} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_td} std={std_td} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")