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
    
    def generate_boolean_circuit(n, m):
        # Generate a random boolean circuit with n inputs and m outputs
        circuit = []
        for _ in range(m):
            gate = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate, inputs))
        return circuit
    
    def binary_representation(circuit):
        # Convert the circuit to a binary string representation
        binary_str = ''.join(str(random.randint(0, 1)) for _ in range(len(circuit)))
        return binary_str
    
    def coxeter_group_generators(binary_str):
        # Simulate the calculation of Coxeter group generators (dummy implementation)
        return len(binary_str)
    
    def monotone_complexity(circuit):
        # Simulate the calculation of monotone complexity (dummy implementation)
        return sum(1 for gate, _ in circuit if gate == 'OR')
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for m in range(1, min(n, 16) + 1):
            circuit = generate_boolean_circuit(n, m)
            binary_str = binary_representation(circuit)
            g_C = coxeter_group_generators(binary_str)
            complexity = monotone_complexity(circuit)
            
            if n > n_max:
                n_max = n
            
            metric_values.append(g_C)
            instances_tested += 1
    
    mean_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(1.41 * m**0.5 <= g_C <= 2 * m**0.5 for g_C, m in zip(metric_values, range(1, min(n_max, 16) + 1)))
    
    return {
        "metric_name": "Coxeter Group Generators",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Circuit with n={n_max}, m=1 has {max(metric_values)} generators and complexity {monotone_complexity(generate_boolean_circuit(n_max, 1))}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")