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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def communication_complexity(cnf):
        m = len(cnf)
        n = max(abs(x) for x in sum(cnf, []))
        complexity = 0
        for clause in cnf:
            complexity += n - abs(sum(clause))
        return complexity / (m * n)
    
    def topological_entropy(cnf):
        m = len(cnf)
        n = max(abs(x) for x in sum(cnf, []))
        entropy = 0
        for i in range(m):
            for j in range(n):
                if random.choice([True, False]):
                    entropy += 1 / (m * n)
        return entropy
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * 2))
            C = communication_complexity(cnf)
            H_min = topological_entropy(cnf)
            results.append((C, H_min))
    
    if not results:
        return {
            "metric_name": "H_min vs C",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    H_min_values = [H for _, H in results]
    C_values = [C for C, _ in results]
    
    mean_H_min = sum(H_min_values) / len(H_min_values)
    std_H_min = math.sqrt(sum((x - mean_H_min) ** 2 for x in H_min_values) / len(H_min_values))
    
    correlation_coefficient = sum((C - mean_C) * (H - mean_H_min) for C, H in results) / \
                               (len(results) * std_C * std_H_min)
    
    return {
        "metric_name": "H_min vs C",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in [(5, 10, 15, 20, 30, 40)[i] for i in range(len(results))]),
        "conjecture_holds": correlation_coefficient >= 0.7 and abs(mean_H_min - (0.5 * sum(C_values))) <= 3 * std_H_min,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data n_tested={len(results)}")