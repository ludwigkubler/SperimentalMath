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
    
    def generate_d_regular_circuit(n, d):
        if n * d % 2 != 0:
            return None
        circuit = []
        for _ in range(d):
            circuit.extend(random.sample(range(1, n), n - 1))
        return circuit
    
    def is_commuting(pair1, pair2):
        return all(circuit[pair1[i]] == circuit[pair2[i]] for i in range(len(pair1)))
    
    def count_commuting_pairs(circuit):
        n = len(circuit) // d
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        return sum(is_commuting(pairs[i], pairs[j]) for i in range(len(pairs)) for j in range(i + 1, len(pairs)))
    
    def compute_geometric_entropy(density_matrix):
        eigenvalues = [sum(row) for row in density_matrix]
        entropy = -sum(eigenvalue * math.log2(eigenvalue) for eigenvalue in eigenvalues if eigenvalue > 0)
        return entropy
    
    def compute_density_matrix(circuit, n):
        density_matrix = [[0] * (n ** 2) for _ in range(n ** 2)]
        for i in range(1 << n):
            state = [i >> j & 1 for j in range(n)]
            output = circuit
            for bit in state:
                if bit == 1:
                    output = [circuit[j] ^ output[j] for j in range(len(output))]
            index = sum(state[i] * (n ** i) for i in range(n))
            density_matrix[index][index] += 1
        return [[entry / (1 << n) for entry in row] for row in density_matrix]
    
    d = 3
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_d_regular_circuit(n, d)
        if circuit is None:
            continue
        
        entanglement_complexity = count_commuting_pairs(circuit)
        
        density_matrix = compute_density_matrix(circuit, n)
        geometric_entropy = compute_geometric_entropy(density_matrix)
        
        results.append({
            "n": n,
            "geometric_entropy": geometric_entropy,
            "entanglement_complexity": entanglement_complexity
        })
    
    if not results:
        return {
            "metric_name": "geometric_entropy_bound",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    geometric_entropy_values = [result["geometric_entropy"] for result in results]
    entanglement_complexity_values = [result["entanglement_complexity"] for result in results]
    
    mean_geometric_entropy = sum(geometric_entropy_values) / instances_tested
    std_geometric_entropy = math.sqrt(sum((x - mean_geometric_entropy) ** 2 for x in geometric_entropy_values) / instances_tested)
    
    conjecture_holds = all(geometric_entropy <= 1.5 * entanglement_complexity for geometric_entropy, entanglement_complexity in zip(geometric_entropy_values, entanglement_complexity_values))
    
    return {
        "metric_name": "geometric_entropy_bound",
        "metric_value": mean_geometric_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean={mean_geometric_entropy}, std={std_geometric_entropy}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean={mean_metric_value}, std={std_metric_value}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")