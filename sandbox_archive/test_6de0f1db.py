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
    
    def generate_random_d_regular_circuit(n, d):
        if n % d != 0:
            return None
        num_nodes = n + 1
        circuit = [[] for _ in range(num_nodes)]
        nodes = list(range(1, num_nodes))
        while len(nodes) > 0:
            node = random.choice(nodes)
            neighbors = random.sample([i for i in range(1, num_nodes) if i != node], d-1)
            circuit[node] = neighbors
            for neighbor in neighbors:
                circuit[neighbor].append(node)
            nodes.remove(node)
        return circuit
    
    def compute_fourier_multiplier_norm(circuit):
        n = len(circuit) - 1
        if n == 0:
            return 0.0
        adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for node, neighbors in enumerate(circuit):
            for neighbor in neighbors:
                adjacency_matrix[node][neighbor] = 1
                adjacency_matrix[neighbor][node] = 1
        
        def gaussian_elimination(A):
            n = len(A)
            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                for j in range(i + 1, n):
                    factor = A[j][i] / A[i][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
            return A
        
        def matrix_norm(A):
            max_row_sum = 0
            for row in A:
                row_sum = sum(abs(x) for x in row)
                if row_sum > max_row_sum:
                    max_row_sum = row_sum
            return max_row_sum
        
        reduced_matrix = gaussian_elimination(adjacency_matrix)
        norm = matrix_norm(reduced_matrix)
        return norm
    
    def compute_entanglement_complexity(circuit):
        n = len(circuit) - 1
        complexity = 0
        for node, neighbors in enumerate(circuit):
            complexity += len(neighbors)
        return complexity / (2 * n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = generate_random_d_regular_circuit(n, 2)
        if circuit is None:
            continue
        norm = compute_fourier_multiplier_norm(circuit)
        complexity = compute_entanglement_complexity(circuit)
        results.append((norm, complexity))
    
    if len(results) == 0:
        return {
            "metric_name": "Fourier Multiplier Norm",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    norm_values, complexity_values = zip(*results)
    mean_norm = sum(norm_values) / len(norm_values)
    max_complexity = max(complexity_values)
    
    return {
        "metric_name": "Fourier Multiplier Norm",
        "metric_value": mean_norm,
        "instances_tested": len(norm_values),
        "n_max": max(n_values),
        "conjecture_holds": all(norm <= 4 * complexity**2 for norm, complexity in results),
        "counterexample": "" if all(norm <= 4 * complexity**2 for norm, complexity in results) else "norm > 4 * complexity^2"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm > 4 * complexity^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")