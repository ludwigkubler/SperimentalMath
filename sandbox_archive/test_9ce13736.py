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
        for _ in range(10 * n):  # Generate 10 clauses per variable
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        seen = set()
        queue = cnf[:]
        while queue:
            literal = queue.pop()
            if literal in seen or -literal in seen:
                continue
            seen.add(literal)
            for clause in cnf:
                if literal in clause:
                    new_clause = [l for l in clause if l != literal and l != -literal]
                    if not new_clause:
                        return len(seen)
                    queue.append(new_clause)
        return len(seen)
    
    n_max = 40
    instances_tested = 30
    r_values = []
    w_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        r_phi = len(cnf)  # Simplified minimal rank for demonstration
        w_phi = resolution_width(cnf)
        
        r_values.append(r_phi)
        w_values.append(w_phi)
    
    correlation_coefficient = sum((r - (sum(r_values) / instances_tested)) * (w - (sum(w_values) / instances_tested)) for r, w in zip(r_values, w_values)) / (instances_tested * math.sqrt(sum((r - (sum(r_values) / instances_tested)) ** 2 for r in r_values)) * math.sqrt(sum((w - (sum(w_values) / instances_tested)) ** 2 for w in w_values)))
    
    conjecture_holds = correlation_coefficient >= 0.8 and all(abs(r_phi - w_phi) <= 3 for r_phi, w_phi in zip(r_values, w_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")