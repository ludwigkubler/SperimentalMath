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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_weight(circuit):
        weight = 0
        for gate, inputs in circuit:
            if gate == 'AND':
                weight += sum(inputs)
            elif gate == 'OR':
                weight += len(inputs) - sum(inputs)
        return weight
    
    def frobenius_schur_indicators(circuit):
        indicators = []
        for _ in range(10):  # Sample 10 random inputs
            input_vector = [random.randint(0, 1) for _ in range(len(circuit))]
            output = 0
            for gate, inputs in circuit:
                if gate == 'AND':
                    output &= sum(input_vector[i] for i in range(len(inputs)))
                elif gate == 'OR':
                    output |= sum(input_vector[i] for i in range(len(inputs)))
            indicators.append(output)
        return indicators
    
    def min_order(indicators):
        indicator_set = set(indicators)
        return len(indicator_set) - 1 if 0 in indicator_set else len(indicator_set)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_boolean_circuit(n)
        weight = compute_weight(circuit)
        indicators = frobenius_schur_indicators(circuit)
        min_order_value = min_order(indicators)
        
        metric_values.append(min_order_value / weight)
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "min_order(FSInd(C)) / weight(C)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_metric >= 0.8 and all(x >= 0.5 for x in metric_values),
        "counterexample": "" if all(x >= 0.5 for x in metric_values) else "metric_value < 0.5"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "metric_value < 0.5" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"metric_value < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")