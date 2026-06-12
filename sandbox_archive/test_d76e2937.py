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
    
    def generate_circuit(n, D):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_circuit(n//2, D-1) for _ in range(2)]
            return [subcircuits[0][i] ^ subcircuits[1][i] for i in range(len(subcircuits[0]))]
    
    def compute_modulus(circuit):
        n = len(circuit)
        adjacency_matrix = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    adjacency_matrix[i][j] = 1
                    adjacency_matrix[j][i] = 1
        return sum(adjacency_matrix[i][j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
    
    def measure_depth(circuit):
        if len(circuit) == 1:
            return 0
        else:
            return max(measure_depth(subcircuit) for subcircuit in circuit) + 1
    
    moduli = []
    depths = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n, random.randint(2, 6))
            moduli.append(compute_modulus(circuit))
            depths.append(measure_depth(circuit))
    
    if not moduli or not depths:
        return {
            "metric_name": "modulus",
            "metric_value": None,
            "instances_tested": len(moduli),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_moduli_or_depths"
        }
    
    mean_modulus = sum(moduli) / len(moduli)
    mean_depth = sum(depths) / len(depths)
    variance_modulus = sum((x - mean_modulus)**2 for x in moduli) / len(moduli)
    variance_depth = sum((x - mean_depth)**2 for x in depths) / len(depths)
    
    if variance_modulus == 0 or variance_depth == 0:
        return {
            "metric_name": "modulus",
            "metric_value": None,
            "instances_tested": len(moduli),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_modulus_or_depth"
        }
    
    std_modulus = math.sqrt(variance_modulus)
    std_depth = math.sqrt(variance_depth)
    
    correlation_coefficient = sum((moduli[i] - mean_modulus) * (depths[i] - mean_depth) for i in range(len(moduli))) / (len(moduli) * std_modulus * std_depth)
    
    return {
        "metric_name": "modulus",
        "metric_value": correlation_coefficient,
        "instances_tested": len(moduli),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")