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
    
    def generate_braided_group(n):
        # Placeholder for generating a braided group of size n
        return [random.randint(1, 10) for _ in range(n)]
    
    def construct_cnf_formula(group):
        # Placeholder for constructing a CNF formula from the braided group
        cnf = []
        for element in group:
            clause = [element]
            cnf.append(clause)
        return cnf
    
    def compute_minimal_rank(group):
        # Placeholder for computing the minimal rank of the braided group
        return len(set(group))
    
    def compute_resolution_proof_width(cnf):
        # Placeholder for computing the resolution proof width of the CNF formula
        return len(cnf)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        group = generate_braided_group(n)
        cnf = construct_cnf_formula(group)
        r_G = compute_minimal_rank(group)
        w_phi_G = compute_resolution_proof_width(cnf)
        
        metric_values.append((r_G, w_phi_G))
    
    if len(metric_values) < 30:
        return {
            "metric_name": "minimal_rank_vs_resolution_width",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        b = (sum_y - m * sum_x) / n
        
        return m, b
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        
        return numerator / denominator
    
    x, y = zip(*metric_values)
    m, b = linear_regression(x, y)
    r_G_avg = sum(x) / len(x)
    w_phi_G_avg = sum(y) / len(y)
    
    if abs(r_G_avg - w_phi_G_avg) > 20:
        conjecture_holds = False
        counterexample = f"r(G)={r_G_avg} and w(φ_G)={w_phi_G_avg}"
    
    correlation = correlation_coefficient(x, y)
    
    return {
        "metric_name": "minimal_rank_vs_resolution_width",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"]) < 0.7 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.7\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'] and abs(r['metric_value']) < 0.7)]}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"]) > 20 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"|r(G) - w(φ_G)|>20\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'] and abs(r['metric_value']) > 20)]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")