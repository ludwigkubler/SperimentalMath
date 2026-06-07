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
    
    def generate_d_regular_circuit(d, n):
        if d * (n - 1) % (2 * n) != 0:
            return None
        circuit = []
        for i in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            row[i] = 1
            circuit.append(row)
        return circuit
    
    def is_commuting(circuit, i, j):
        n = len(circuit)
        for k in range(n):
            if (circuit[i][k] * circuit[j][i] != circuit[j][k] * circuit[i][j]):
                return False
        return True
    
    def compute_entanglement_complexity(circuit):
        n = len(circuit)
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                if is_commuting(circuit, i, j):
                    complexity += 1
        return complexity
    
    def compute_density_matrix(circuit, n):
        density_matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if is_commuting(circuit, i, j):
                    density_matrix[i][j] += Fraction(1)
                    density_matrix[j][i] += Fraction(1)
                else:
                    density_matrix[i][j] -= Fraction(1)
                    density_matrix[j][i] -= Fraction(1)
        for i in range(n):
            density_matrix[i][i] += Fraction(1)
        return density_matrix
    
    def compute_geometric_entropy(density_matrix, n):
        trace = sum(density_matrix[i][i] for i in range(n))
        if trace <= 0:
            return None
        entropy = -trace * math.log(trace) / (n * math.log(n))
        return entropy
    
    d = random.randint(2, 4)
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_d_regular_circuit(d, n)
    
    if circuit is None:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entanglement_complexity = compute_entanglement_complexity(circuit)
    density_matrix = compute_density_matrix(circuit, n)
    geometric_entropy = compute_geometric_entropy(density_matrix, n)
    
    if geometric_entropy is None:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    conjecture_holds = geometric_entropy <= 1.5 * entanglement_complexity
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": geometric_entropy,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Geometric entropy {geometric_entropy} > 1.5 * Entanglement complexity {entanglement_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif sum(r["conjecture_holds"] for r in results) >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")