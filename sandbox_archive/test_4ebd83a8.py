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
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate in circuit:
            if gate[0] == 'NOT':
                stack.append(not input_values[gate[1]])
            elif gate[0] == 'AND':
                stack.append(stack.pop() and input_values[gate[1]])
            elif gate[0] == 'OR':
                stack.append(stack.pop() or input_values[gate[1]])
        return stack[-1]
    
    def find_min_cubes(circuit):
        n = len(circuit)
        output_values = set()
        for i in range(2**n):
            input_values = {j: (i >> j) & 1 for j in range(n)}
            output_values.add(evaluate_circuit(circuit, input_values))
        
        cubes = []
        for value in output_values:
            cube = [0] * n
            for i in range(n):
                if evaluate_circuit(circuit, {j: (value >> j) & 1 for j in range(i)}) != evaluate_circuit(circuit, {j: (value >> j) & 1 for j in range(i+1)}):
                    cube[i] = 1
            cubes.append(cube)
        
        return len(cubes)
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        k = random.randint(5, 40)
        circuit = []
        for i in range(k):
            gate_type = random.choice(['NOT', 'AND', 'OR'])
            if gate_type == 'NOT':
                input_index = random.randint(0, len(circuit) - 1)
                circuit.append(('NOT', input_index))
            else:
                input_indices = random.sample(range(len(circuit)), 2)
                circuit.append((gate_type, input_indices[0], input_indices[1]))
        
        num_cubes = find_min_cubes(circuit)
        expected_bound = k**2 * math.log(n_max)
        
        if abs(num_cubes - expected_bound) > 1e-6:
            conjecture_holds = False
            counterexample = f"n={len(circuit)}, k={k}, num_cubes={num_cubes}, expected_bound={expected_bound}"
    
    metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": "Number of distinct cubes",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")