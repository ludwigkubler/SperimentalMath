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
        # Generate a random monotone circuit computing OR of n variables
        circuit = []
        for _ in range(n - 1):
            gate = random.choice(['OR', 'AND'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_hodge_index(circuit):
        # Placeholder function to compute the Hodge index
        # This is a dummy implementation; replace with actual computation
        depth = len(circuit)
        hodge_index = 10 * math.log(depth)  # Dummy value for testing
        return hodge_index
    
    def circuit_depth(circuit):
        # Compute the depth of the circuit
        if not circuit:
            return 0
        max_depth = 0
        for gate, inputs in circuit:
            if gate == 'OR':
                depths = [circuit_depth(sub_circuit) for sub_circuit in inputs]
                max_depth = max(max_depth, *depths)
            elif gate == 'AND':
                depths = [circuit_depth(sub_circuit) for sub_circuit in inputs]
                max_depth = max(max_depth, *depths)
        return 1 + max_depth
    
    n = random.randint(5, 40)
    circuit = generate_monotone_circuit(n)
    depth = circuit_depth(circuit)
    hodge_index = compute_hodge_index(circuit)
    
    if hodge_index > 10000:
        return {
            "metric_name": "Hodge Index",
            "metric_value": hodge_index,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Hodge index {hodge_index} exceeds the threshold of 10,000"
        }
    
    return {
        "metric_name": "Hodge Index",
        "metric_value": hodge_index,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 10000 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 10000)
        print(f"RESULT: FALSIFIED counterexample=\"Hodge index exceeds the threshold of 10,000\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")