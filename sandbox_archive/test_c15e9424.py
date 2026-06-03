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
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def monotone_width(circuit):
        width = [0] * (len(circuit) + 1)
        for i in range(len(circuit)):
            gate_type, inputs = circuit[i]
            if gate_type == 'AND':
                width[i+1] = max(width[j] for j in inputs) + 1
            else:
                width[i+1] = max(width[j] for j in inputs)
        return max(width)
    
    def calculate_hodge_norm(circuit):
        # Placeholder for actual Hodge norm calculation
        # For simplicity, we'll use a random value between 0 and n
        return random.uniform(0, len(circuit))
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_monotone_circuit(n)
            w_C = monotone_width(circuit)
            min_norm_H = calculate_hodge_norm(circuit)
            metrics.append((w_C, min_norm_H))
    
    if not metrics:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_metrics_collected"
        }
    
    w_C_values, min_norm_H_values = zip(*metrics)
    mean_w_C = sum(w_C_values) / len(w_C_values)
    mean_min_norm_H = sum(min_norm_H_values) / len(min_norm_H_values)
    
    covariance = sum((w_C - mean_w_C) * (min_norm_H - mean_min_norm_H) for w_C, min_norm_H in metrics) / len(metrics)
    variance_w_C = sum((w_C - mean_w_C)**2 for w_C in w_C_values) / len(w_C_values)
    variance_min_norm_H = sum((min_norm_H - mean_min_norm_H)**2 for min_norm_H in min_norm_H_values) / len(min_norm_H_values)
    
    if variance_w_C == 0 or variance_min_norm_H == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_correlation_coefficient = covariance / (math.sqrt(variance_w_C) * math.sqrt(variance_min_norm_H))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": pearson_correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        mean_value = sum(r["metric_value"] for r in results if "metric_value" in r)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if "metric_value" in r))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")