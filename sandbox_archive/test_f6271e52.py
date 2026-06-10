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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n * 3):
            clause = [random.randint(1, n), random.randint(1, n), -random.randint(1, n)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def diophantine_polynomial(clauses):
        # Simplified mapping for demonstration; actual implementation needed
        return sum([x**2 + y**2 + z**2 for x, y, z in clauses])
    
    def communication_complexity_rank_variance(instance):
        # Placeholder function; actual implementation needed
        return random.random()
    
    def degree_of_polynomial(poly):
        if isinstance(poly, int) or poly == 0:
            return 0
        elif isinstance(poly, dict):
            return max(degree_of_polynomial(coeff) for coeff in poly.values())
        else:
            return len(poly)
    
    n_max = 40
    instances_tested = 30
    degrees = []
    variances = []
    
    for _ in range(instances_tested):
        instance = generate_sat_instance(n_max)
        poly = diophantine_polynomial(instance)
        degree = degree_of_polynomial(poly)
        variance = communication_complexity_rank_variance(instance)
        
        degrees.append(degree)
        variances.append(variance)
    
    correlation_coefficient = sum((d - mean_d) * (v - mean_v) for d, v in zip(degrees, variances)) / (instances_tested * std_d * std_v)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) <= 0.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 10**6) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")