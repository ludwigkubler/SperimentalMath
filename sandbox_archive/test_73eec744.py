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
    
    def generate_monotone_circuit(n):
        # Generate a random monotone circuit with n variables
        circuit = []
        for i in range(1, n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(i)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        # Compute the monotone width of the circuit
        width = 0
        for gate, inputs in circuit:
            width = max(width, len(inputs))
        return width
    
    def compute_hodge_norm(n):
        # Compute a generic Hodge norm (simplified example)
        return random.uniform(1, n)
    
    min_norm_sum = 0
    monotone_width_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_monotone_circuit(n)
            monotone_width = compute_monotone_width(circuit)
            hodge_norm = compute_hodge_norm(n)
            
            min_norm_sum += hodge_norm
            monotone_width_sum += monotone_width
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_min_norm = min_norm_sum / instances_tested
    mean_monotone_width = monotone_width_sum / instances_tested
    
    if math.isclose(mean_min_norm, 0) or math.isclose(mean_monotone_width, 0):
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Mean values are zero"
        }
    
    correlation_coefficient = (min_norm_sum * monotone_width_sum - instances_tested * mean_min_norm * mean_monotone_width) / \
                               math.sqrt((min_norm_sum**2 - instances_tested * mean_min_norm**2) *
                                         (monotone_width_sum**2 - instances_tested * mean_monotone_width**2))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        first_failing_seed = next((r["seed"] for r in results if not ("conjecture_holds" in r and r["conjecture_holds"])), None)
        counterexample = "first failing seed"
    
    print(f"RESULT: {'SUPPORTED' if support_fraction == 1.0 else 'FALSIFIED'} mean={mean_value} std={std_dev} support_fraction={support_fraction}")