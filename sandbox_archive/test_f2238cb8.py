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
    
    def generate_monotone_circuit(n):
        circuit = []
        for _ in range(2**(n-1)):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def monotone_width(circuit):
        stack = []
        max_inputs = 0
        for gate, inputs in circuit:
            if gate == 'AND':
                stack.append(len(inputs))
                max_inputs = max(max_inputs, len(inputs))
            elif gate == 'OR':
                stack.append(1)
        return max_inputs
    
    def hodge_class_norm(circuit):
        width = monotone_width(circuit)
        # Simplified Hodge class norm calculation
        return Fraction(width, 2**width)
    
    n_values = [5, 10, 15, 20, 30, 40]
    norms = []
    widths = []
    
    for n in n_values:
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
            "counterexample": "Empty circuit generated"
        }
    
    mean_norm = sum(norms) / len(norms)
    mean_width = sum(widths) / len(widths)
    
    covariance = sum((norm - mean_norm) * (width - mean_width) for norm, width in zip(norms, widths)) / len(norms)
    variance_norm = sum((norm - mean_norm)**2 for norm in norms) / len(norms)
    variance_width = sum((width - mean_width)**2 for width in widths) / len(widths)
    
    if variance_norm == 0 or variance_width == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(norms),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Zero variance in norms or widths"
        }
    
    pearson_coefficient = covariance / (math.sqrt(variance_norm) * math.sqrt(variance_width))
    
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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Pearson coefficient < 0.8\" first_failing_seed={r['seed']}")
                break