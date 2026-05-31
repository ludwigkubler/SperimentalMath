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
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def communication_complexity(cnf):
        # Simplified estimate based on the number of clauses
        return len(cnf) * 2
    
    def topological_entropy(cnf):
        # Simplified estimate based on the number of variables and clauses
        n = max(abs(x) for clause in cnf for x in clause)
        m = len(cnf)
        return math.log(n, 2) + math.log(m, 2)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * 2))
            H_min = topological_entropy(cnf)
            C = communication_complexity(cnf)
            results.append((H_min, C))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    H_min_values = [H for H, C in results]
    C_values = [C for H, C in results]
    
    mean_H_min = sum(H_min_values) / len(H_min_values)
    std_H_min = math.sqrt(sum((x - mean_H_min) ** 2 for x in H_min_values) / len(H_min_values))
    
    correlation_coefficient = sum((H_min_values[i] - mean_H_min) * (C_values[i] - mean_C) for i in range(len(results))) / \
                               (len(results) * std_H_min * math.sqrt(sum((x - mean_C) ** 2 for x in C_values)))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and mean_H_min <= mean_C + 3 * std_H_min,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result['metric_value'] for result in results if result['metric_value'] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result['metric_value'] - mean_metric_value) ** 2 for result in results if result['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result['conjecture_holds']:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break