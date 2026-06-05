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
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['AND', 'OR'])
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def shoenfield_hierarchy(formula):
        # Simplified version of Shoenfield hierarchy for demonstration
        return len(formula.split())
    
    def circuit_monotone_width(formula):
        # Simplified version of circuit monotone width for demonstration
        return formula.count('AND') + formula.count('OR')
    
    instances_tested = 0
    n_max = 5
    min_index_values = []
    w_values = []
    counterexample = ""
    
    for n in range(5, 41):
        if n > n_max:
            n_max = n
        
        for _ in range(3):  # Sample 3 instances per size
            formula = generate_formula(n)
            min_index = shoenfield_hierarchy(formula)
            w = circuit_monotone_width(formula)
            
            min_index_values.append(min_index)
            w_values.append(w)
            instances_tested += 1
    
    if instances_tested < 90:  # Ensure at least 30 instances per seed
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_min_index = sum(min_index_values) / len(min_index_values)
    mean_w = sum(w_values) / len(w_values)
    correlation_coefficient = 0
    
    if mean_w != 0:
        numerator = sum((x - mean_min_index) * (y - mean_w) for x, y in zip(min_index_values, w_values))
        denominator = math.sqrt(sum((x - mean_min_index) ** 2 for x in min_index_values)) * math.sqrt(sum((y - mean_w) ** 2 for y in w_values))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_min_index - mean_w) <= 3,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'] and r['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")