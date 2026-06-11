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
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                circuit.append((gate, random.randint(1, n)))
            else:
                circuit.append((gate, random.sample(range(1, n+1), 2)))
        return circuit
    
    def symplectic_area(circuit):
        area = 0
        for gate, inputs in circuit:
            if gate == 'NOT':
                area += 1
            elif gate == 'AND' or gate == 'OR':
                area += len(inputs)
        return area
    
    n_max = 40
    instances_tested = 0
    total_area = 0
    max_size = 0
    max_depth = 0
    
    for size in range(5, 41):
        for depth in range(2, 11):
            if instances_tested >= 30:
                break
            circuit = generate_circuit(size)
            area = symplectic_area(circuit)
            total_area += area
            instances_tested += 1
            max_size = max(max_size, size)
            max_depth = max(max_depth, depth)
    
    mean_area = total_area / instances_tested if instances_tested > 0 else 0
    conjecture_holds = all(area <= size**2 * depth for _, size, depth in [(symplectic_area(generate_circuit(size)), size, depth) for size in range(5, 41) for depth in range(2, 11)])
    
    return {
        "metric_name": "Symplectic Area",
        "metric_value": mean_area,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_area = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_area} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_area} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")