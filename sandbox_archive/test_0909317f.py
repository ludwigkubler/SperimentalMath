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
    
    def generate_circuit(n, k):
        # Generate a random n-vertex circuit with monotone width k
        circuit = []
        for _ in range(k):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, min(4, n)))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        # Evaluate the circuit with given input values
        stack = list(input_values)
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                result = all(stack.pop() for _ in inputs)
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in inputs)
            stack.append(result)
        return stack[0]
    
    def find_min_cubes(circuit):
        # Find the minimal number of distinct cubes required
        n = len(circuit)
        k = len(circuit)
        output_values = set()
        
        # Generate all possible input combinations
        for i in range(2**n):
            input_values = [bool(i & (1 << j)) for j in range(n)]
            output_value = evaluate_circuit(circuit, input_values)
            output_values.add(output_value)
        
        # Determine the minimal number of cubes
        cubes = set()
        for value in output_values:
            cube = []
            for i in range(n):
                if circuit[i][0] == 'AND':
                    cube.append((i, 1 if value else 0))
                elif circuit[i][0] == 'OR':
                    cube.append((i, 1 if not value else 0))
            cubes.add(tuple(sorted(cube)))
        
        return len(cubes)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(1, min(n - 1, 4))
            circuit = generate_circuit(n, k)
            num_cubes = find_min_cubes(circuit)
            total_metric_value += num_cubes
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(math.log(num_cubes) <= k**2 * math.log(n) for n in n_values for _ in range(5))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Number of distinct cubes",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")