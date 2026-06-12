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

def generate_circuit(n, D):
    if n == 1:
        return [random.choice([0, 1])]
    else:
        depth = random.randint(1, min(D, n-1))
        circuit = []
        for _ in range(depth):
            subcircuit = generate_circuit(n - 1, D - depth)
            gate = random.choice(['AND', 'OR'])
            circuit.append((gate, subcircuit))
        return circuit

def compute_modulus(circuit):
    n = len(circuit) + 1
    adjacency_matrix = [[0] * n for _ in range(n)]
    
    def dfs(node, parent):
        if isinstance(node, tuple):
            gate, children = node
            for child in children:
                adjacency_matrix[node][child] = 1
                adjacency_matrix[child][node] = 1
                dfs(child, node)
    
    dfs(0, None)
    
    return sum(adjacency_matrix[i][j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    moduli = []
    depths = []
    
    for n in n_values:
        for _ in range(5):  # 5 instances per size
            circuit = generate_circuit(n, random.randint(5, 40))
            moduli.append(compute_modulus(circuit))
            depths.append(len(circuit) + 1)
    
    if not moduli or not depths:
        return {
            "metric_name": "modulus",
            "metric_value": 0.0,
            "instances_tested": len(moduli),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_moduli_or_depths"
        }
    
    mean_modulus = sum(moduli) / len(moduli)
    mean_depth = sum(depths) / len(depths)
    correlation_coefficient = 0.0
    
    if len(moduli) > 1:
        numerator = sum((moduli[i] - mean_modulus) * (depths[i] - mean_depth) for i in range(len(moduli)))
        denominator = math.sqrt(sum((moduli[i] - mean_modulus) ** 2 for i in range(len(moduli))) * sum((depths[i] - mean_depth) ** 2 for i in range(len(depths))))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0.0
    
    return {
        "metric_name": "modulus",
        "metric_value": mean_modulus,
        "instances_tested": len(moduli),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_modulus = sum(r['metric_value'] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r['metric_value'] - mean_modulus) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_modulus} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")