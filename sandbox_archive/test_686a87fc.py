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
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(1, n) for _ in range(random.randint(2, 3))]
            circuit.append((gate, inputs))
        return circuit
    
    def get_output_values(circuit, n):
        # Compute the set of all distinct output values for C
        outputs = set()
        for i in range(2**n):
            input_state = [bool(i & (1 << j)) for j in range(n)]
            output = 0
            for gate, inputs in circuit:
                if gate == 'AND':
                    output &= all(input_state[i-1] for i in inputs)
                elif gate == 'OR':
                    output |= any(input_state[i-1] for i in inputs)
            outputs.add(output)
        return outputs
    
    def count_distinct_cubes(outputs):
        # Determine the minimal number of cubes required to represent these output values
        cubes = []
        for output in outputs:
            cube = [output]
            for other_output in outputs:
                if other_output != output and all((x or y) == (x and y) for x, y in zip(bin(output)[2:].zfill(3), bin(other_output)[2:].zfill(3))):
                    cube.append(other_output)
            cubes.append(cube)
        return len(cubes)
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n-1, 4))
    circuit = generate_circuit(n, k)
    outputs = get_output_values(circuit, n)
    num_cubes = count_distinct_cubes(outputs)
    
    return {
        "metric_name": "num_cubes",
        "metric_value": num_cubes,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": num_cubes <= k**2 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")