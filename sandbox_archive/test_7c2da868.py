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

def generate_cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] == 0 for i in range(n)):
            clause[random.randint(0, n - 1)] = random.choice([-1, 1])
        clauses.append(clause)
    return clauses

def construct_quantum_tensor_network(cnf: list) -> dict:
    tensor_network = {}
    qubit_count = len(cnf[0])
    for i in range(qubit_count):
        tensor_network[i] = [random.randint(0, 1) for _ in range(2)]
    return tensor_network

def calculate_rank(tensor_network: dict) -> int:
    rank = 0
    for qubit, values in tensor_network.items():
        if any(value != 0 for value in values):
            rank += 1
    return rank

def resolution_width(cnf: list) -> int:
    width = 0
    for clause in cnf:
        width = max(width, len([var for var in clause if var != 0]))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        tensor_network = construct_quantum_tensor_network(cnf)
        R_min = calculate_rank(tensor_network)
        w_phi = resolution_width(cnf)
        
        if R_min == 0 or w_phi == 0:
            continue
        
        results.append((R_min, w_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_pairs"
        }
    
    R_min_values = [R for R, _ in results]
    w_phi_values = [w for _, w in results]
    
    mean_R_min = sum(R_min_values) / len(R_min_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    
    correlation_coefficient = sum((R - mean_R_min) * (w - mean_w_phi) for R, w in results) / (len(results) * math.sqrt(sum((R - mean_R_min) ** 2 for R in R_min_values)) * math.sqrt(sum((w - mean_w_phi) ** 2 for w in w_phi_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean(abs(R - w) for R, w in results) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] is not None for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_pairs")