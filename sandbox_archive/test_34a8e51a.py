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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(n), 2))
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_entanglement_complexity(circuit):
        n = len(circuit) + 1
        complexity = 0
        for gate in circuit:
            if gate[0] == 'AND':
                complexity += 1
            elif gate[0] == 'OR':
                complexity += 1
        return complexity
    
    def compute_barycentric_coordinates(circuit):
        n = len(circuit) + 1
        coordinates = set()
        for i in range(2**n):
            point = [int(x) for x in format(i, f'0{n}b')]
            valid = True
            for gate in circuit:
                if gate[0] == 'AND':
                    if point[gate[1][0]] + point[gate[1][1]] != 2:
                        valid = False
                        break
                elif gate[0] == 'OR':
                    if point[gate[1][0]] + point[gate[1][1]] != 1:
                        valid = False
                        break
            if valid:
                coordinates.add(tuple(point))
        return len(coordinates)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = generate_random_circuit(n)
        entanglement_complexity = compute_entanglement_complexity(circuit)
        barycentric_coordinates = compute_barycentric_coordinates(circuit)
        results.append((n, entanglement_complexity, barycentric_coordinates))
    
    total_n = sum(1 for n, _, _ in results)
    mean_ratio = sum(b / e for n, e, b in results) / total_n
    std_dev = math.sqrt(sum((b / e - mean_ratio)**2 for n, e, b in results) / total_n)
    
    support_fraction = sum(abs(b / e - 1) <= 0.1 for n, e, b in results) / total_n
    
    return {
        "metric_name": "Ratio of Barycentric Coordinates to Entanglement Complexity",
        "metric_value": mean_ratio,
        "instances_tested": total_n,
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": "" if support_fraction >= 0.95 else "Ratio exceeds ±20%"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - 1) <= 0.1) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - 1) > 0.2 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - 1) > 0.2)
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds ±20%' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")