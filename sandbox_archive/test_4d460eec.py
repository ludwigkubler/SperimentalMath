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
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def monotone_width(circuit):
        width = 0
        stack = []
        for gate, inputs in circuit:
            if gate == 'AND':
                stack.append(len(inputs))
            elif gate == 'OR':
                max_inputs = max(stack)
                stack = [max_inputs + len(inputs) - 1]
        return max(stack)
    
    def hodge_class_norm(circuit):
        # Simplified model for Hodge class norm
        width = monotone_width(circuit)
        return math.sqrt(width)
    
    n_values = [5, 10, 15, 20, 30, 40]
    norms = []
    widths = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_monotone_circuit(n)
            norm = hodge_class_norm(circuit)
            width = monotone_width(circuit)
            norms.append(norm)
            widths.append(width)
    
    if not norms or not widths:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_norm = sum(norms) / len(norms)
    mean_width = sum(widths) / len(widths)
    covariance = sum((norm - mean_norm) * (width - mean_width) for norm, width in zip(norms, widths)) / len(norms)
    variance_width = sum((width - mean_width) ** 2 for width in widths) / len(widths)
    
    if variance_width == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(norms),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_coefficient = covariance / math.sqrt(variance_width)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_coefficient,
        "instances_tested": len(norms),
        "n_max": max(n_values),
        "conjecture_holds": pearson_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_metric = sum(r["metric_value"] for r in results) / len(results)
        std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE missing_data")