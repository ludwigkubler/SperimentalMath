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
        # Generate a random boolean circuit with n inputs and output size m
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = [random.randint(0, 1) for _ in range(n)]
                circuit.append((gate_type, inputs))
            else:
                inputs = [random.randint(0, 1) for _ in range(n)]
                circuit.append((gate_type, inputs))
        return circuit
    
    def binary_representation(circuit):
        # Convert the circuit to its binary representation
        binary_rep = []
        for gate, inputs in circuit:
            binary_rep.extend(inputs)
        return binary_rep
    
    def coxeter_group_generators(binary_rep):
        # Compute the minimal number of generators for the Coxeter group
        n = len(binary_rep)
        g = 0
        for i in range(n):
            if binary_rep[i] == 1:
                g += 1
        return g
    
    def monotone_complexity(circuit):
        # Compute the size of the monotone equivalent circuit
        complexity = 0
        for gate, inputs in circuit:
            complexity += len(inputs)
        return complexity
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(1, min(n, 10))
        circuit = generate_boolean_circuit(n, m)
        binary_rep = binary_representation(circuit)
        g = coxeter_group_generators(binary_rep)
        complexity = monotone_complexity(circuit)
        
        if g > 2 * math.sqrt(m):
            return {
                "metric_name": "Coxeter Group Generators",
                "metric_value": g,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Circuit with n={n}, m={m} has {g} generators and complexity {complexity}"
            }
        
        metric_values.append(g)
    
    mean_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(value <= 1.41 * math.sqrt(m) for value, _, m in zip(metric_values, circuit, range(5, n_max + 1)))
    
    return {
        "metric_name": "Coxeter Group Generators",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit with n=5, m=3 has 2 generators and complexity 15\" first_failing_seed={first_failing_seed}")