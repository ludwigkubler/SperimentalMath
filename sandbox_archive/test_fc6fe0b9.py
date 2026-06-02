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
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_local_cohomology(cnf):
        # Simplified local cohomology computation
        lcoh = len(cnf) / n
        return lcoh
    
    def measure_frege_proof_length(cnf):
        # Placeholder for Frege proof length calculation
        # This is a dummy implementation and should be replaced with actual logic
        f_phi = 10 * len(cnf)
        return f_phi
    
    def correlation_coefficient(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    lcoh_values = []
    f_phi_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        lcoh = compute_local_cohomology(cnf)
        f_phi = measure_frege_proof_length(cnf)
        
        lcoh_values.append(lcoh)
        f_phi_values.append(f_phi)
    
    correlation_coefficient_value = correlation_coefficient(lcoh_values, f_phi_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient_value,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient_value < 0.7,
        "counterexample": "" if 0.5 <= correlation_coefficient_value < 0.7 else "correlation_coefficient_out_of_range"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "correlation_coefficient_out_of_range" for r in results):
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_out_of_range' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_other_reasons")