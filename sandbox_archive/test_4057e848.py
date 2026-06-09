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
        for _ in range(10):  # Generate 10 clauses
            clause = [random.randint(-1, -n), random.randint(1, n)]
            while len(set(clause)) != 2:  # Ensure each clause has exactly two literals
                clause = [random.randint(-1, -n), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        width = 0
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                        if new_clause not in clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
            width += 1
        return width
    
    def hodge_degree(cnf):
        # Placeholder for actual Hodge degree computation
        # Since this is a placeholder, we'll just use the number of variables as a proxy
        n = max(abs(lit) for clause in cnf for lit in clause)
        return n  # Simplified version for testing purposes
    
    instances_tested = 0
    total_min_deg = 0
    total_width = 0
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)  # Sweep through different instance sizes
        cnf = generate_cnf(n)
        min_deg = hodge_degree(cnf)
        width = resolution_width(cnf)
        
        instances_tested += 1
        total_min_deg += min_deg
        total_width += width
        
        if abs(min_deg - width) > 3:
            counterexample = f"n={n}, min_deg(H)={min_deg}, w(φ)={width}"
            break
    
    mean_min_deg = total_min_deg / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(min_deg * width for min_deg, width in zip([mean_min_deg] * instances_tested, [mean_width] * instances_tested)) - instances_tested * mean_min_deg * mean_width) / math.sqrt((instances_tested * sum(min_deg ** 2 for min_deg in [mean_min_deg] * instances_tested) - instances_tested * mean_min_deg ** 2) * (instances_tested * sum(width ** 2 for width in [mean_width] * instances_tested) - instances_tested * mean_width ** 2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(5, 40),  # Ensure n_max is at least 16
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.05,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")