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
        circuit = []
        for _ in range(k):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(1, n) for _ in range(gate == 'AND')]
            circuit.append((gate, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result = all(input_values[i-1] for i in inputs)
            elif gate == 'OR':
                result = any(input_values[i-1] for i in inputs)
            stack.append(result)
        return stack.pop()
    
    def min_cubes_to_represent(circuit, n):
        input_space_size = 2 ** n
        output_values = set(evaluate_circuit(circuit, [i % 2 for i in range(1, input_space_size + 1)]) for _ in range(input_space_size))
        cubes = []
        for value in output_values:
            cube = [0] * n
            for i in range(n):
                if (value >> i) & 1:
                    cube[i] = 1
            cubes.append(cube)
        return len(cubes)
    
    def monotone_width(circuit):
        max_depth = 0
        stack = []
        for gate, inputs in reversed(circuit):
            depth = max(stack[-i-1] if i < len(stack) else 0 for i in inputs) + 1
            stack.append(depth)
            max_depth = max(max_depth, depth)
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, min(n-1, 5))
        circuit = generate_circuit(n, k)
        num_cubes = min_cubes_to_represent(circuit, n)
        results.append({
            "n": n,
            "k": k,
            "num_cubes": num_cubes
        })
    
    total_num_cubes = sum(result["num_cubes"] for result in results)
    mean_num_cubes = total_num_cubes / len(results)
    std_dev = math.sqrt(sum((result["num_cubes"] - mean_num_cubes) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["num_cubes"] <= k**2 * math.log(n) for result in results)
    counterexample = "" if conjecture_holds else f"n={result['n']}, k={result['k']}, num_cubes={result['num_cubes']}"
    
    return {
        "metric_name": "Number of distinct cubes",
        "metric_value": mean_num_cubes,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")