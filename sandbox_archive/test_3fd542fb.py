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
    
    def generate_ac0_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                result = all(input_values[i] for i in inputs)
            elif gate_type == 'OR':
                result = any(input_values[i] for i in inputs)
            stack.append(result)
        return stack.pop()
    
    def tropical_representation(circuit):
        n = len(circuit)
        input_values = [random.randint(0, 1) for _ in range(n)]
        output = evaluate_circuit(circuit, input_values)
        
        # Convert output to binary string
        binary_output = bin(output)[2:]
        
        # Count distinct tropical representations
        distinct_representations = len(set(binary_output))
        
        # Determine the maximum order of a monomial
        max_order = max(len(segment) for segment in binary_output.split('0'))
        
        return distinct_representations, max_order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        distinct_representations, max_order = tropical_representation(circuit)
        
        if distinct_representations < math.ceil(n ** (1/3)) or max_order < math.ceil(n ** (1/3)):
            counterexample = f"n={n}, distinct_representations={distinct_representations}, max_order={max_order}"
            return {
                "metric_name": "Distinct Tropical Representations and Max Order",
                "metric_value": 0,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append((distinct_representations, max_order))
    
    return {
        "metric_name": "Distinct Tropical Representations and Max Order",
        "metric_value": sum(results) / len(results),
        "instances_tested": n_values[-1],
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= math.ceil(n_values[-1] ** (1/3))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r < math.ceil(n_values[-1] ** (1/3)) for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        counterexample = f"n={n_values[-1]}, distinct_representations={min(results)}, max_order=0"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")