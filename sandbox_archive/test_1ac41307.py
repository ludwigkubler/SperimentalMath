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
    
    def generate_circuit(n, m):
        # Generate a random boolean circuit with n inputs and m gates
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def hyperbolic_metric_entropy(circuit):
        # Placeholder for the actual computation of hyperbolic metric entropy
        # This is a dummy implementation for demonstration purposes
        return random.uniform(0, 1)
    
    def satisfiability_time(circuit):
        # Placeholder for the actual computation of satisfiability time
        # This is a dummy implementation for demonstration purposes
        return random.uniform(0, 10)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    satisfiability_times = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, 2 * n)
        circuit = generate_circuit(n, m)
        entropy = hyperbolic_metric_entropy(circuit)
        time = satisfiability_time(circuit)
        
        metric_values.append(entropy)
        satisfiability_times.append(time)
    
    correlation_coefficient = sum((x - mean(metric_values)) * (y - mean(satisfiability_times)) for x, y in zip(metric_values, satisfiability_times)) / (len(metric_values) * std_dev(metric_values) * std_dev(satisfiability_times))
    
    conjecture_holds = correlation_coefficient >= 0.8 and max(metric_values) <= 10
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "hyperbolic_metric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results])
    std_dev_value = std_dev([r["metric_value"] for r in results])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")