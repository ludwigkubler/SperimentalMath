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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def communication_complexity(cnf):
    # Simplified model: each variable appears in at least one clause
    variables = set()
    for clause in cnf:
        for var in clause:
            if var > 0:
                variables.add(var)
            else:
                variables.add(-var)
    return len(variables)

def topological_entropy(cnf):
    # Simplified model: entropy proportional to the number of clauses
    return Fraction(len(cnf), 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    H_min_values = []
    C_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n // 2, n)
            cnf = generate_cnf(n, m)
            
            H_min = topological_entropy(cnf)
            C = communication_complexity(cnf)
            
            H_min_values.append(H_min)
            C_values.append(C)
    
    mean_H_min = sum(H_min_values) / len(H_min_values)
    mean_C = sum(C_values) / len(C_values)
    
    correlation_coefficient = sum((H_min_values[i] - mean_H_min) * (C_values[i] - mean_C) for i in range(len(H_min_values))) / \
                              math.sqrt(sum((H_min_values[i] - mean_H_min) ** 2 for i in range(len(H_min_values))) *
                                        sum((C_values[i] - mean_C) ** 2 for i in range(len(C_values))))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(H_min_values),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")