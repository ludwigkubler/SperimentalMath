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
        return [[random.randint(-n, n) for _ in range(3)] for _ in range(random.randint(1, 5))]
    
    def dpll_search_tree_diameter(instance):
        n = len(instance[0])
        initial_model = [None] * n
        
        def dfs(model, depth):
            if all([any([model[abs(l) - 1] == l // abs(l) for l in clause]) for clause in instance]):
                return depth
            unsatisfied_clauses = [clause for clause in instance if not any([model[abs(l) - 1] == l // abs(l) for l in clause])]
            if not unsatisfied_clauses:
                return float('inf')
            literal = random.choice(unsatisfied_clauses[0])
            new_model_true = model[:]
            new_model_false = model[:]
            new_model_true[abs(literal) - 1] = literal // abs(literal)
            new_model_false[abs(literal) - 1] = -(literal // abs(literal))
            return min(dfs(new_model_true, depth + 1), dfs(new_model_false, depth + 1))
        
        return dfs(initial_model, 0)
    
    def p_adic_hodge_structure(instance):
        n = len(instance[0])
        # Simplified mapping for demonstration
        return sum([sum(abs(l) for l in clause) for clause in instance]) / (n * n)
    
    instances_tested = 30
    metric_values = []
    n_max = 40
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = generate_instance(n)
        d = dpll_search_tree_diameter(instance)
        mH_G = p_adic_hodge_structure(instance)
        
        if d == float('inf'):
            continue
        
        metric_values.append(mH_G / (d ** 0.25))
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(0.9 <= x / (d ** 0.25) <= 1.1 for d, mH_G in zip(dpll_search_tree_diameter(instance), p_adic_hodge_structure(instance)) for _ in range(instances_tested))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mH(G) / d^(1/4)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")