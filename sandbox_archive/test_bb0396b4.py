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
    
    def generate_circuit(n, D):
        circuit = []
        for _ in range(D):
            layer = [random.choice([0, 1]) for _ in range(n)]
            circuit.append(layer)
        return circuit
    
    def compute_modulus(circuit):
        n = len(circuit[0])
        adjacency_matrix = [[0] * n for _ in range(n)]
        for layer in circuit:
            for i in range(n):
                for j in range(i + 1, n):
                    if layer[i] != layer[j]:
                        adjacency_matrix[i][j] += 1
                        adjacency_matrix[j][i] += 1
        return sum(sum(row) for row in adjacency_matrix) / (n * (n - 1))
    
    def measure_depth(circuit):
        return len(circuit)
    
    n = random.randint(5, 30)
    D = random.randint(5, 40)
    circuit = generate_circuit(n, D)
    moduli = [compute_modulus(circuit) for _ in range(30)]
    depths = [measure_depth(circuit) for _ in range(30)]
    
    correlation_coefficient = sum((moduli[i] - mean(moduli)) * (depths[i] - mean(depths)) for i in range(len(moduli))) / (len(moduli) * std(moduli) * std(depths))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(D),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def std(values):
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results])
    std_value = std([r["metric_value"] for r in results])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")