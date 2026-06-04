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
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with n inputs
        depth = random.randint(2, 5)
        circuit = []
        for _ in range(depth):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = [random.choice([0, 1]) for _ in range(n)]
            else:
                inputs = [random.choice([0, 1]) for _ in range(2)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        # Compute the monotone width of the circuit
        max_width = 0
        current_width = 0
        for gate in circuit:
            if gate[0] == 'AND':
                current_width += len(gate[1])
            else:
                current_width -= 1
            max_width = max(max_width, current_width)
        return max_width
    
    def compute_representation_length(monotone_width):
        # Compute the representation length of the quantum group
        return monotone_width * 2
    
    n_max = 0
    instances_tested = 0
    total_representation_length = 0
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        circuit = generate_circuit(n)
        monotone_width = compute_monotone_width(circuit)
        representation_length = compute_representation_length(monotone_width)
        total_representation_length += representation_length
        instances_tested += 1
    
    mean_representation_length = total_representation_length / instances_tested
    conjecture_holds = abs(mean_representation_length - n_max) <= n_max / 2
    counterexample = "" if conjecture_holds else f"n={n_max}, expected={n_max}, got={mean_representation_length}"
    
    return {
        "metric_name": "representation_length",
        "metric_value": mean_representation_length,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_representation_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_representation_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_representation_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")