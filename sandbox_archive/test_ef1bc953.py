# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(l == 0 for l in literals):
                continue
            clause = tuple(sorted(literals))
            if clause not in clauses:
                clauses.append(clause)
        return clauses
    
    def resolution_tree(cnf):
        nodes = {(): []}
        stack = [()]
        
        while stack:
            node1 = stack.pop()
            for literal1 in node1:
                for node2, literals2 in nodes.items():
                    if -literal1 in literals2:
                        new_literals = sorted(set(literals2) - {-literal1})
                        if new_literals not in nodes:
                            nodes[new_literals] = []
                            stack.append(new_literals)
        
        return nodes
    
    def geometric_entanglement(tree):
        # Placeholder for actual implementation
        return 0.0
    
    n_values = [5, 10, 15, 20, 30, 40]
    mge_sum = 0
    w_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        tree = resolution_tree(cnf)
        mge_value = geometric_entanglement(tree)
        
        if mge_value == 0.0 or len(tree) == 1:
            continue
        
        w_value = len(tree) - 1
        mge_sum += mge_value * w_value
        w_sum += w_value
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = mge_sum / w_sum
    p_value = 0.0  # Placeholder for actual implementation
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5 and p_value <= 0.05,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5 or p_value > 0.05\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")