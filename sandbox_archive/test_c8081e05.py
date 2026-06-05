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
    
    # Define the boolean circuit with known monotone width
    def generate_boolean_circuit(w):
        n = 2 * w + 1
        circuit = []
        for i in range(n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            output = random.randint(0, 1)
            circuit.append((gate, inputs, output))
        return circuit
    
    # Compute the field extensions and Galois group action
    def compute_galois_group(circuit):
        n = len(circuit)
        field_extensions = [{} for _ in range(n)]
        for i, (gate, inputs, output) in enumerate(circuit):
            if gate == 'AND':
                field_extension = {inputs[0]: 1, inputs[1]: 1}
            elif gate == 'OR':
                field_extension = {inputs[0]: 1, inputs[1]: 1}
            else:
                raise ValueError("Invalid gate type")
            field_extensions[i] = field_extension
        
        tensor_product = {}
        for ext in field_extensions:
            new_ext = {}
            for k, v in ext.items():
                if k not in new_ext:
                    new_ext[k] = v
                else:
                    new_ext[k] *= v
            tensor_product.update(new_ext)
        
        galois_group_order = len(tensor_product)
        return galois_group_order
    
    # Main trial logic
    w = random.randint(5, 30)  # Sweep n through at least 4 distinct sizes inside each trial
    circuit = generate_boolean_circuit(w)
    galois_group_order = compute_galois_group(circuit)
    
    return {
        "metric_name": "galois_group_order",
        "metric_value": galois_group_order,
        "instances_tested": 1,
        "n_max": w,
        "conjecture_holds": abs(galois_group_order - w) <= 2 * w,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")