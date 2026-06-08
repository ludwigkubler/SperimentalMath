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
        clauses = []
        for _ in range(2**n):  # Generate a random CNF formula with n variables
            clause = [random.randint(-1, 1) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def ehrhart_polynomial_degree(clauses):
        # Placeholder function to compute the degree of the Ehrhart polynomial
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(clauses)  # Simplified for demonstration purposes
    
    def clause_depth(clause):
        return max(abs(x) for x in clause)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    degrees = [ehrhart_polynomial_degree(cnf)]
    depths = [sum(clause_depth(c) for c in cnf)]
    
    if not degrees or not depths:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": 0.0,
            "instances_tested": len(degrees),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_degree = sum(degrees) / len(degrees)
    mean_depth = sum(depths) / len(depths)
    correlation_coefficient = (len(degrees) * sum(d * e for d, e in zip(depths, degrees)) - 
                               sum(depths) * sum(degrees)) / math.sqrt(
                                   (len(degrees) * sum(d**2 for d in depths) - sum(depths)**2) *
                                   (len(degrees) * sum(e**2 for e in degrees) - sum(degrees)**2))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(degrees),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")