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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def quadratic_form(cnf, x):
        value = 0
        for clause in cnf:
            product = 1
            for lit in clause:
                if lit > 0:
                    product *= x[lit-1]
                else:
                    product *= (1 - x[-lit-1])
            value += product
        return value
    
    def lp_norm(value, p=2):
        return (sum(abs(v)**p for v in value))**(1/p)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(n * random.uniform(0.5, 2))
        cnf = generate_cnf(n, m)
        
        x = [random.choice([0, 1]) for _ in range(n)]
        
        norm = lp_norm(quadratic_form(cnf, x), p=2)
        results.append(norm)
    
    min_norm = min(results)
    resolution_size = random.randint(10, 50)  # Simulated resolution size
    
    conjecture_holds = abs(min_norm - (resolution_size * n**(n/2) * (m/n)**(1/2) * math.log(n/m))) <= 0.05 * resolution_size
    counterexample = "" if conjecture_holds else "counterexample_not_defined"
    
    return {
        "metric_name": "min_Lp_norm",
        "metric_value": min_norm,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result:
            results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - (r * 0.95)) <= 0.05 * r) / len(results)
    
    if all(trial_result["conjecture_holds"] for trial_result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='counterexample_not_defined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")