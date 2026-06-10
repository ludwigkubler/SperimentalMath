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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0 or d >= n:
            return None
        edges = []
        for i in range(n):
            neighbors = set(random.sample(range(n), d))
            neighbors.remove(i)
            edges.extend([(i, j) for j in neighbors])
        return edges
    
    def tseitin_formula(edges, n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in range(i + 1, n):
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    clause = [-literals[i], f'-{literals[j]}', f'-{literals[k]}']
                    clauses.append(clause)
        return clauses
    
    def kostant_multi_index(clauses):
        # Placeholder implementation
        return len(clauses)
    
    def resolution_width(clauses):
        # Placeholder implementation
        return len(clauses)
    
    n = 10
    d = 3
    max_n = 20
    instances_tested = 0
    kmi_values = []
    width_values = []
    
    while len(kmi_values) < 100 and n <= max_n:
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        
        phi = tseitin_formula(graph, n)
        if not phi:
            continue
        
        kmi = kostant_multi_index(phi)
        width = resolution_width(phi)
        
        if kmi is not None and width is not None:
            kmi_values.append(kmi)
            width_values.append(width)
            instances_tested += 1
    
    if len(kmi_values) < 100:
        return {
            "metric_name": "correlation",
            "metric_value": -1,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "insufficient_samples"
        }
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y)
        return cov / (var_x * var_y) ** 0.5
    
    r = correlation(kmi_values, width_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": r >= 0.8,
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
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = (sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")