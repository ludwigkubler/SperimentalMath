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
    
    def generate_braided_group(n):
        # Placeholder for generating a braided group
        return [random.randint(1, n) for _ in range(n)]
    
    def construct_cnf_formula(group):
        # Placeholder for constructing a CNF formula from the braided group
        cnf = []
        for i in range(len(group)):
            clause = [group[i], -group[(i + 1) % len(group)]]
            cnf.append(clause)
        return cnf
    
    def compute_minimal_rank(group):
        # Placeholder for computing the minimal rank of a braided group
        n = len(group)
        rank = 0
        for i in range(n):
            if group[i] not in group[:i]:
                rank += 1
        return rank
    
    def compute_resolution_proof_width(cnf):
        # Placeholder for computing the resolution proof width of a CNF formula
        width = max(len(clause) for clause in cnf)
        return width
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        group = generate_braided_group(n)
        cnf = construct_cnf_formula(group)
        
        minimal_rank = compute_minimal_rank(group)
        resolution_width = compute_resolution_proof_width(cnf)
        
        metric_values.append((minimal_rank, resolution_width))
    
    if not metric_values:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_r = sum(r for r, _ in metric_values)
    total_w = sum(w for _, w in metric_values)
    mean_r = total_r / instances_tested
    mean_w = total_w / instances_tested
    
    correlation_coefficient = 0
    if len(metric_values) > 1:
        numerator = sum((r - mean_r) * (w - mean_w) for r, w in metric_values)
        denominator = math.sqrt(sum((r - mean_r)**2 for r, _ in metric_values)) * math.sqrt(sum((w - mean_w)**2 for _, w in metric_values))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.95 and all(abs(r - w) <= 10 * w for r, w in metric_values)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r['conjecture_holds']) > 7:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")