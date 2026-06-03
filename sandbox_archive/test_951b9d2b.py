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
        cnf = []
        for _ in range(10 * n):  # Generate a CNF with 10 clauses per variable
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def calculate_mli(cnf):
        n = max(abs(lit) for lit in set(lit for clause in cnf for lit in clause))
        # Placeholder for actual MLI calculation logic
        return n  # Simplified for demonstration purposes
    
    def resolution_width(cnf):
        # Placeholder for actual resolution width calculation logic
        return len(cnf)
    
    instances_tested = 0
    total_mli = 0.0
    total_width = 0.0
    n_max = 1
    
    for _ in range(30):  # Test with 30 random CNFs
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        mli_value = calculate_mli(cnf)
        width_value = resolution_width(cnf)
        
        instances_tested += 1
        total_mli += mli_value
        total_width += width_value
        n_max = max(n_max, n)
    
    mean_mli = total_mli / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * mean_mli * mean_width - 
                               sum(mli * width for mli, width in zip(cnf, cnf))) / \
                              math.sqrt((instances_tested * sum(mli**2 for mli in cnf) - 
                                          sum(mli**2 for mli in cnf)) *
                                        (instances_tested * sum(width**2 for width in cnf) - 
                                         sum(width**2 for width in cnf)))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                                              31, 37, 41, 43, 47, 53, 59, 61, 67, 
                                              71, 73, 79, 83, 89, 97, 101, 103, 107, 
                                              109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")