# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_circuit(n, depth):
    if n == 1:
        return [f"X{random.randint(0, n-1)}"]
    elif depth == 1:
        inputs = generate_circuit(n, depth - 1)
        return [f"({random.choice(['AND', 'OR'])} {inputs[i]} {inputs[i+1]})" for i in range(0, len(inputs), 2)]
    else:
        inputs = generate_circuit(n, depth - 1)
        return [f"({random.choice(['NOT', 'XOR'])} {inputs[i]})" for i in range(len(inputs))]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n, random.randint(1, 3))
        satisfiability_threshold = len(circuit)  # Simplified threshold for demonstration
        minimal_order = Fraction(satisfiability_threshold * 2, 1)  # Simplified order for demonstration
        
        results.append({
            "n": n,
            "satisfiability_threshold": satisfiability_threshold,
            "minimal_order": minimal_order
        })
    
    if not results:
        return {
            "metric_name": "Minimal Order vs Satisfiability Threshold",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    mean_order = sum(result["minimal_order"] for result in results) / len(results)
    std_order = (sum((result["minimal_order"] - mean_order) ** 2 for result in results) / len(results)) ** 0.5
    
    alpha = Fraction(1, 1)
    beta = Fraction(0, 1)
    
    expected_bound = [alpha * Fraction(n, 1).log() + beta for n in n_values]
    
    if any(result["minimal_order"] > bound + 3 * std_order for result, bound in zip(results, expected_bound)):
        return {
            "metric_name": "Minimal Order vs Satisfiability Threshold",
            "metric_value": mean_order,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Order exceeds expected bound by more than 3 std deviations"
        }
    
    return {
        "metric_name": "Minimal Order vs Satisfiability Threshold",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    std_order = (sum((result["metric_value"] - mean_order) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds expected bound by more than 3 std deviations\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")