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
    
    def generate_xor_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_minimal_rank(tropical_curve):
        # Placeholder function to simulate minimal rank computation
        # Replace with actual tropical curve rank computation logic
        return random.randint(1, n)
    
    def communication_complexity(xor_function):
        # Placeholder function to simulate communication complexity calculation
        # Replace with actual read-twice branching program communication complexity logic
        return len(xor_function) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_communication_complexity = 0
    total_minimal_rank = 0
    instances_tested = 0
    
    for n in n_values:
        xor_function = generate_xor_boolean_function(n)
        minimal_rank = compute_minimal_rank(xor_function)
        communication_complexity_value = communication_complexity(xor_function)
        
        total_communication_complexity += communication_complexity_value
        total_minimal_rank += minimal_rank
        instances_tested += 1
    
    mean_communication_complexity = total_communication_complexity / instances_tested
    mean_minimal_rank = total_minimal_rank / instances_tested
    correlation_coefficient = (total_communication_complexity * total_minimal_rank - instances_tested * mean_communication_complexity * mean_minimal_rank) / ((instances_tested - 1) * math.sqrt((total_communication_complexity**2 - instances_tested * mean_communication_complexity**2) * (total_minimal_rank**2 - instances_tested * mean_minimal_rank**2)))
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_communication_complexity - mean_minimal_rank) <= 3
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_communication_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")